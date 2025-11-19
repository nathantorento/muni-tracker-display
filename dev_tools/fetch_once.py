# dev_tools/fetch_once.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from src.muni import fetch_muni_data

# Default: J inbound at 20th / Right Of Way
STOP_ID_DEFAULT = "16215"

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "sample_data" / "sample_response.json"

def main(stop_code: str = STOP_ID_DEFAULT):
    print(f"Fetching data for stop {stop_code} ...")

    data = fetch_muni_data(stop_code, use_cached=False)

    if not data:
        print("API returned no data.")
        return

    # Ensure directory exists
    OUTPUT_FILE.parent.mkdir(exist_ok=True, parents=True)

    # Save the JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    arrivals = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
    print(f"Saved {len(arrivals)} arrivals to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
