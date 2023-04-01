import time
import numpy as np
from bs4 import BeautifulSoup

from mpc_params import *
from road_defs import *

def create_dua_demand(T, sim_time, directory):

    #filename = "pregen_demand.txt"

    zeros_array = np.zeros(int(sim_time/T)+1, dtype=int)

    dua_veh_katip_s = zeros_array.tolist()
    dua_veh_katip_n = zeros_array.tolist()
    dua_veh_aurora_w = zeros_array.tolist()
    dua_veh_aurora_e = zeros_array.tolist()

    # Reading data from the xml file
    with open(directory, "r") as f:
        data = f.read()

    soup = BeautifulSoup(data, "xml")
    print("Successfully parsed the DUArouter route file")

    f.close()

    #print(soup.prettify())

    trips = soup.find_all("tripinfo")
    
    #print(trips)

    i = 0
    j = 0
    arrival = 0.0

    while arrival < 50400.0:

        arrival = float(trips[i]["arrival"])
        departing_lane = trips[i]["departLane"]
        j = int(arrival/float(T))

        if departing_lane in katip_south_edges:
            dua_veh_katip_s[j] += 1
        elif departing_lane in katip_north_edges:
            dua_veh_katip_n[j] += 1
        elif departing_lane in aurora_west_edges:
            dua_veh_aurora_w[j] += 1
        elif departing_lane in aurora_east_edges:
            dua_veh_aurora_e[j] += 1

        i += 1

        #print(f"departure = {departure}")
        #print(f"departing_lane = {departing_lane}")
        #print(f"j = {j}")

    print(f"Successfully read demand definitions for {T} s intervals")

    dua_veh_katip_s.pop(0)
    dua_veh_katip_n.pop(0)
    dua_veh_aurora_w.pop(0)
    dua_veh_aurora_e.pop(0)

    return np.array(dua_veh_katip_s), np.array(dua_veh_katip_n), np.array(dua_veh_aurora_w), np.array(dua_veh_aurora_e)