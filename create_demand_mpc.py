# Author: Jan Lendl R. Uy
# CoE 199 Demand Generation by Reading Trips File

import numpy as np
from bs4 import BeautifulSoup
import time
from road_defs import *

def create_dua_demand(T, sim_time, directory):

    #filename = "pregen_demand.txt"

    zeros_array = np.zeros(int(sim_time/T+0.5)+1, dtype=int)

    dua_veh_katip_s = zeros_array.tolist()
    dua_veh_katip_n = zeros_array.tolist()
    dua_veh_aurora_w = zeros_array.tolist()
    dua_veh_aurora_e = zeros_array.tolist()

    dua_veh_aurora_e_katip_s = zeros_array.tolist()
    dua_veh_aurora_e_aurora_w = zeros_array.tolist()
    dua_veh_aurora_e_prop_constants = zeros_array.tolist()

    # Reading data from the xml file
    with open(directory, "r") as f:
        data = f.read()

    soup = BeautifulSoup(data, "xml")
    print("Successfully parsed the DUArouter route file")

    f.close()

    #print(soup.prettify())

    trips = soup.find_all("tripinfo")

    i = 0
    j = 0
    depart = 0.0

    while depart < 50400.0:

        depart = float(trips[i]["depart"])
        departing_lane = trips[i]["departLane"]
        arrival_lane = trips[i]["arrivalLane"]
        j = int(depart/float(T))

        if depart >= 50400.0:
            break

        if departing_lane in katip_south_edges:
            dua_veh_katip_s[j] += 1
        elif departing_lane in katip_north_edges:
            dua_veh_katip_n[j] += 1
        elif departing_lane in aurora_west_edges:
            dua_veh_aurora_w[j] += 1
        else:
            dua_veh_aurora_e[j] += 1
            if arrival_lane in katip_south_arrival_lanes:
                dua_veh_aurora_e_katip_s[j] += 1
            elif arrival_lane in aurora_west_arrival_lanes:
                dua_veh_aurora_e_aurora_w[j] += 1
        
        i += 1

    print(f"Successfully read demand definitions for {T} s intervals")

    return np.array(dua_veh_katip_s), np.array(dua_veh_katip_n), np.array(dua_veh_aurora_w), np.array(dua_veh_aurora_e), np.array(dua_veh_aurora_e_katip_s)