from pprint import pprint

from muni import get_muni_arrivals
from utils import convert_to_pst, time_until_arrival_minutes

# 🚧 TEST MODE ENABLED: Using cached API data and simulating "now" as 5 min before arrival

# Relevant Stop IDs
STOP_ID_J_INBOUND = "16215" #Right Of Way/20th St to Downtown
# STOP_ID_J_OUTBOUND = "16214" #Right Of Way/20th St to Balboa Park
# STOP_ID_33_WESTBOUND = "13323"  #18th St & Church St to The Richmond District
# STOP_ID_33_EASTBOUND = "13322" #18th St & Church St to San Francisco General Hospital

if __name__ == "__main__":
    # Toggle this depending on if you're debugging
    stop_code = STOP_ID_J_INBOUND

    # Use cached data while testing to avoid API rate limit
    transit_info = get_muni_arrivals(stop_code, use_cached=True)

    if transit_info:
        try:
            visits = transit_info["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]
            closest_transit = visits[0]
            arrival_time = closest_transit["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]

            sf_time = convert_to_pst(arrival_time)
            minutes_away = time_until_arrival_minutes(arrival_time)

            # print(f"Arrival time: {sf_time}")
            print(f"J is {minutes_away} minutes")

        except (KeyError, IndexError) as e:
            print(f"Error parsing transit data: {e}")
    else:
        print("No data received.")
