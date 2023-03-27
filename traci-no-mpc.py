# Authors: Eisler Spencer Go, Jan Lendl R. Uy
# Interfacing of SUMO simulation via TraCI

# Conventions
# KatipS: Katipunan Southbound / Katipunan North
# KatipN: Katipunan Northbound / Katipunan South
# AuroW: Aurora Westbound / Aurora East
# AuroE: Aurora Eastbound / Aurora West

import os
import sys
import time

import traci
import traci.constants as tc
import numpy as np

import performance_indicators as perf
import save_sim_results as save_sim

# Declaration of environment variable
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# Directory of sumo-gui and sumocfg files
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:\\Users\\lendl\\Documents\\smart_traffic\\sumo\\25-3-simfile.sumocfg"]

# Starts the simulation
traci.start(sumoCmd)

# Junction IDs and Traffic Light IDs
junctionID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'
trafficlightID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'

#traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

# Actual simulation
# Entire simulation spans from 6AM to 8PM traffic (14 hrs/50400 secs)
# 1 step corresponds to 1 second

sim_duration = 50400 # Fixed

step_C = 0
allcar={}
stopped_vehs = {}

n_aurora_west = 0
n_aurora_east = 0
sumcar = 0

# Record start time of simulation for optimization purposes
start = time.time()

for step in range(sim_duration):

    delta_step = step-step_C

    hr, mins, sec, am_pm = perf.convert_to_real_time(step)
    print(f"Timestep: {step}")
    print(f"Current time step relative to new phase: {delta_step}")
    print(f"{hr}:{mins}:{sec} {am_pm}")
    
    # Get the average queue time of all incoming roads
    qt_katip_south, qt_katip_north, qt_aurora_west, qt_aurora_east = perf.get_avg_wait()
      
    # Get the average flow rate of all incoming roads
    traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 60)

    #totalcarflow = perf.get_car_flow("all")
   
    if step > 0:
        flow_katip_south = perf.get_flow_rate("KatipS")
        flow_katip_north = perf.get_flow_rate("KatipN")
        flow_aurora_west = perf.get_flow_rate("AuroraW")
        flow_aurora_east = perf.get_flow_rate("AuroraE")

    # "Snapshot" of vehicles that are stationary (for queue length)
    # Ensures that recorded stationary vehicles belong to the queue
    new_stopped_vehs = perf.get_queue_length(stopped_vehs, 1, step)

    # Obtain average queueing time of all incoming roads
    if delta_step > 0:
        ql_katip_south, ql_katip_north, ql_aurora_west, ql_aurora_east, new_stopped_vehs = perf.get_queue_length(new_stopped_vehs, 0, step)

    # Obtain vehicle count in all incoming roads
    n_katip_south, n_katip_north, n_aurora_west, n_aurora_east = perf.get_vehicle_count("all")

    # Obtain cumulative number of vehicles inserted in the simulation since time 0
    spawned_katip_south, spawned_katip_north, spawned_aurora_west, spawned_aurora_east = perf.get_spawned_vehs()

    # Record traffic data for each time step except zeroth second
    if step == 0:
        continue

    save_sim.write_results([n_katip_south, n_katip_north, n_aurora_west, n_aurora_east],
                           [ql_katip_south, ql_katip_north, ql_aurora_west, ql_aurora_east],
                           [qt_katip_south, qt_katip_north, qt_aurora_west, qt_aurora_east], 
                           [flow_katip_south, flow_katip_north, flow_aurora_west, flow_aurora_east],
                           [spawned_katip_south, spawned_katip_north, spawned_aurora_west, spawned_aurora_east],
                           step)

    # Step the simulation by 1 second
    traci.simulationStep()
    print("\n")

traci.close()

# Record start time of simulation for optimization purposes
print(f"Runtime of simulation: {time.time()-start}")