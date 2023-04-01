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

from mpc_params import *
from mpc import *

import performance_indicators as perf
import save_sim_results as save_sim

# Declaration of environment variable
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# Directory of sumo-gui and sumocfg files
with open("sumoBinary.txt") as f:
    sumoBinary = f.readline()
with open("sumoCmd.txt") as f:
    sumoFolder = f.readline()
# sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", sumoFolder]

# Starts the simulation
traci.start(sumoCmd)

# Junction IDs and Traffic Light IDs
junctionID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'
trafficlightID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'

#traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

# Actual simulation
# Entire simulation spans from 6AM to 8PM traffic (14 hrs/50400 secs)

step_len = 0.5
steps_per_s = int(1/step_len)
sim_duration = int(50400/step_len) # Fixed

# Record start time of simulation for optimization purposes
start = time.time()

# Obtain initial timer settings and cycle time
u, C = do_mpc()
u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
step_C = 0

allcar={}
stopped_vehs = {}

#ql_sampling_time = 2

print(f"u = {u_sorted}")
print(f"C = {C}")
print(f"phases = {phases}")

n_aurora_west = 0
n_aurora_east = 0

sumcar = 0
for step in range(sim_duration):

    #dummy_delta_step = step-step_C
    
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
    if step > 0:
        ql_katip_south, ql_katip_north, ql_aurora_west, ql_aurora_east, new_stopped_vehs = perf.get_queue_length(new_stopped_vehs, 0, step)

    # Obtain cumulative number of vehicles inserted in the simulation since time 0
    spawned_katip_south, spawned_katip_north, spawned_aurora_west, spawned_aurora_east = perf.get_spawned_vehs()

    # Obtain vehicle count in all incoming roads
    n_katip_south, n_katip_north, n_aurora_west, n_aurora_east = perf.get_vehicle_count("all")

    # Record traffic data for each time step except zeroth second
    if step == 0:
        traci.simulationStep()
        continue

    if step%steps_per_s == 1:

        delta_step = (step//steps_per_s)-step_C

        hr, mins, sec, am_pm = perf.convert_to_real_time(step//steps_per_s)
        print(f"Timestep: {step//steps_per_s}")
        print(f"Current time step relative to new phase: {delta_step}")
        print(f"{hr}:{mins}:{sec} {am_pm}")

        # Perform switching of phases based on the current time step
        # Adjusts timer settings of all stoplights based on computed green times
        if delta_step == 0:
            # Handle skipping of phases
            if (u_sorted[0] == u_sorted[1] == 0) and (u_sorted[3]>0):
                traci.trafficlight.setPhase(trafficlightID, 2)
                traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[3])
            else:
                traci.trafficlight.setPhase(trafficlightID, 0)
                traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[0])
            print(f"Timer applied: {u_sorted[0]} s")
        elif delta_step == phases[1]-3:
            traci.trafficlight.setPhase(trafficlightID, 1)
            traci.trafficlight.setPhaseDuration(trafficlightID, 3)
            print(f"Timer applied: 3 s")
        elif delta_step == phases[1]:
            traci.trafficlight.setPhase(trafficlightID, 2)
            traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[3])
            n_aurora_east_fair = n_aurora_east # Save vehicle count for Aurora East (just before green time)
            print(f"Timer applied: {u_sorted[3]} s")
        elif delta_step == phases[2]-3:
            traci.trafficlight.setPhase(trafficlightID, 3)
            traci.trafficlight.setPhaseDuration(trafficlightID, 3)
            print(f"Timer applied: 3 s")
        elif delta_step == phases[2]:
            traci.trafficlight.setPhase(trafficlightID, 4)
            traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[2])
            n_aurora_west_fair = n_aurora_west # Save vehicle count for Aurora West (just before green time)
            print(f"Timer applied: {u_sorted[2]} s")
        elif delta_step == C-3:
            traci.trafficlight.setPhase(trafficlightID, 5)
            traci.trafficlight.setPhaseDuration(trafficlightID, 3)
            print(f"Timer applied: 3 s")

        phase_num = traci.trafficlight.getPhase(trafficlightID)

        print(f"Current phase number: {phase_num}")

        save_sim.write_results([n_katip_south, n_katip_north, n_aurora_west, n_aurora_east],
                            [ql_katip_south, ql_katip_north, ql_aurora_west, ql_aurora_east],
                            [qt_katip_south, qt_katip_north, qt_aurora_west, qt_aurora_east], 
                            [flow_katip_south, flow_katip_north, flow_aurora_west, flow_aurora_east],
                            step//steps_per_s, u_sorted, C)
        
        # print(sumcar)
        # Perform MPC once a control interval has completed
        if delta_step+1 == C:
            print("Performing MPC to compute optimal green times!")
            # Recompute timer settings and cycle time
            u, C = do_mpc(np.array([n_katip_south, n_katip_north, n_aurora_west_fair, n_aurora_east_fair]), (step//steps_per_s)+1)
            u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
            '''
            if (u or C) == None:
                C = u_sorted[0]+u_sorted[3]+u_sorted[2]+9
            else:
                u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
            '''
            step_C = (step//steps_per_s)+1
        
            print(f"u = {u_sorted}")
            print(f"C = {C}")
            print(f"phases = {phases}")

    # Step the simulation by 1 second
    traci.simulationStep()
    print("\n")

traci.close()

# Record start time of simulation for optimization purposes
print(f"Runtime of simulation: {time.time()-start}")