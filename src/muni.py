# src/muni.py

import os
import json
from pathlib import Path
from typing import List, TypedDict, Optional

import requests

from src.utils_time import convert_to_pst, time_until_arrival_minutes

API_KEY = os.getenv("MUNI_API_KEY")
BASE_URL = "https://api.511.org/transit/StopMonitoring"
CACHE_FILE = Path(__file__).resolve().parent.parent / "sample_data" / "sample_response.json"

class Arrival(TypedDict):
    """
    Parsed arrival details ready for display on the dashboard after extraction from the 511.org API.
    """
    line: str
    destination: str
    expected_time_utc: str
    expected_time_local: str
    minutes_away: int

def fetch_muni_data(stop_code: str, use_cached: bool = False) -> Optional[dict]:
    """
    Fetch real-time Muni stop data for a given stop code.

    If use_cached is True and a cache file exists, returns the cached JSON instead
    of calling the API for development and testing purposes.
    """
    if use_cached and CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Cached JSON is invalid: {e}")
            # fall through to a live request

    if not API_KEY and not use_cached:
        print("Missing MUNI_API_KEY environment variable.")
        return None

    if use_cached and not CACHE_FILE.exists():
        print("Cache file does not exist; falling back to live API call.")

    params = {
        "api_key": API_KEY,
        "agency": "SF",
        "stopcode": stop_code,
        "format": "json",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        # Handle possible BOM in response
        text = response.content.decode("utf-8-sig")
        data = json.loads(text)

        # Save cache for future offline / test use
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return data

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

def parse_arrivals(transit_info: dict) -> List[Arrival]:
    """
    Parse the Muni StopMonitoring API response into a simple list of arrivals.

    Each arrival includes:
      - line (e.g. "J")
      - destination (e.g. "Embarcadero Station")
      - expected_time_utc (ISO 8601 string)
      - expected_time_local (formatted SF time string)
      - minutes_away (int)
    """
    arrivals: List[Arrival] = []

    try:
        visits = transit_info["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    except (KeyError, TypeError):
        print("Unexpected response shape: missing MonitoredStopVisit list.")
        return arrivals

    for visit in visits:
        try:
            journey = visit["MonitoredVehicleJourney"]
            call = journey["MonitoredCall"]

            line = journey.get("LineRef", "Unknown")
            destination = call.get("DestinationDisplay", "Unknown destination")
            expected_utc = call["ExpectedArrivalTime"]

            local_str = convert_to_pst(expected_utc)
            minutes = time_until_arrival_minutes(expected_utc)

            arrivals.append(
                {
                    "line": line,
                    "destination": destination,
                    "expected_time_utc": expected_utc,
                    "expected_time_local": local_str,
                    "minutes_away": minutes,
                }
            )
        except KeyError as e:
            # Skip broken records but keep going
            print(f"Skipping one visit due to missing field: {e}")
            continue

    return arrivals
