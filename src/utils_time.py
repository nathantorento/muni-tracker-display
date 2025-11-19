# src/utils_time.py

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

SF_TZ = ZoneInfo("America/Los_Angeles")

def convert_to_pst(utc_iso_str: str) -> str:
    """
    Convert a UTC ISO time string to a San Francisco local time string.
    Example input: "2025-06-27T22:18:15Z"
    Example output: "03:18 PM (PDT)"
    """
    utc_time = datetime.fromisoformat(utc_iso_str.replace("Z", "+00:00"))
    local_time = utc_time.astimezone(SF_TZ)
    return local_time.strftime("%I:%M %p (%Z)")

def time_until_arrival_minutes(
        arrival_iso_str: str, 
        now: datetime | None = None) -> int:
    """
    Return the number of whole minutes between 'now' and the arrival time.
    """
    arrival_time = datetime.fromisoformat(arrival_iso_str.replace("Z", "+00:00"))
    
    if now is None:
        now = datetime.now(timezone.utc)

    diff_minutes = int((arrival_time - now).total_seconds() // 60)
    return diff_minutes
