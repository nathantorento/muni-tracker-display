import os
import json
import requests
from pathlib import Path

API_KEY = os.getenv("MUNI_API_KEY")
CACHE_FILE = Path("sample_response.json")

def get_muni_arrivals(stop_code: str, use_cached: bool = False) -> dict | None:
    """
    Retrieves and optionally caches Muni real-time stop data when given the exact stop code.

    Args:
        stop_code (str): The Muni stop ID.
        use_cached (bool): If True, loads from local file instead of making request.

    Returns:
        dict | None: The API response or cached data.
    """
    if use_cached and CACHE_FILE.exists():
        print("📂 Loaded cached sample_response.json")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    url = (
        f"https://api.511.org/transit/StopMonitoring?"
        f"api_key={API_KEY}&agency=SF&stopcode={stop_code}&format=json"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        raw_text = response.content.decode("utf-8-sig")
        data = json.loads(raw_text)

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
