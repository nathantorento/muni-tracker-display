from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

def convert_to_pst(utc_iso_str):
    """
    Converts a UTC ISO time string to San Francisco local time string.
    """
    utc_time = datetime.fromisoformat(utc_iso_str.replace("Z", "+00:00"))
    local_time = utc_time.astimezone(ZoneInfo("America/Los_Angeles"))
    return local_time.strftime("%I:%M %p (%Z)")

def time_until_arrival_minutes(arrival_iso_str, simulate_5_min_before=True):
    """
    Returns the number of minutes between now and the arrival time.
    Optionally simulates 'now' as 5 minutes before arrival (for testing).
    """
    arrival_time = datetime.fromisoformat(arrival_iso_str.replace("Z", "+00:00"))
    
    if simulate_5_min_before:
        time_now = arrival_time - timedelta(minutes=5)
    else:
        time_now = datetime.now(timezone.utc)

    diff = (arrival_time - time_now).total_seconds() // 60
    return int(diff)