# src/main.py

from dotenv import load_dotenv
load_dotenv()

from src.muni import fetch_muni_data, parse_arrivals
from src.render_dashboard import render_dashboard
from src.config import (
    STOP_ID_J_INBOUND,
    STOP_ID_J_OUTBOUND,
    STOP_ID_33_WESTBOUND,
    STOP_ID_33_EASTBOUND,
    MAX_ARRIVALS,
)

def build_entry(line_label, direction_label, arrivals, max_items=3):
    """Format parsed arrival data for dashboard entries."""
    if not arrivals:
        return {
            "line": line_label,
            "destination": direction_label,
            "times": "No service"
        }

    times = ", ".join(
        str(a["minutes_away"]) for a in arrivals[:max_items]
    )

    return {
        "line": line_label,
        "destination": direction_label,
        "times": times
    }

def get_arrivals(stop_id):
    data = fetch_muni_data(stop_id, use_cached=False)
    if not data:
        return []
    return parse_arrivals(data)

def main():
    # Fetch + parse for each stop
    j_in = get_arrivals(STOP_ID_J_INBOUND)
    j_out = get_arrivals(STOP_ID_J_OUTBOUND)
    bus_33_w = get_arrivals(STOP_ID_33_WESTBOUND)
    bus_33_e = get_arrivals(STOP_ID_33_EASTBOUND)

    # Build entries for dashboard
    entries = [
        build_entry("J", "Downtown (Inbound)", j_in, max_items=MAX_ARRIVALS),
        build_entry("J", "Balboa Park (Outbound)", j_out, max_items=MAX_ARRIVALS),
        build_entry("33", "The Richmond (Westbound)", bus_33_w, max_items=MAX_ARRIVALS),
        build_entry("33", "SF General Hospital (Eastbound)", bus_33_e, max_items=MAX_ARRIVALS),
    ]

    render_dashboard(entries)

if __name__ == "__main__":
    main()
