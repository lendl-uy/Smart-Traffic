# Authors: Eisler Spencer Go, Jan Lendl R. Uy
# Interfacing of SUMO simulation via TraCI

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
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:\\Users\\lendl\\Documents\\smart_traffic\\sumo\\micro\\003\\iteration_003.sumocfg"]

# Starts the simulation
traci.start(sumoCmd)

# Junction IDs and Traffic Light IDs
junctionID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'
trafficlightID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'

step_len = 0.5
steps_per_s = int(1/step_len)
sim_duration = int(50400/step_len) # Fixed

allcar={}
stopped_vehs = {}

n_aurora_west = 0
n_aurora_east = 0

sumcar = 0

# Actual simulation
# Entire simulation spans from 6AM to 8PM traffic (14 hrs/50400 secs)
# 1 step corresponds to 0.5 seconds

def main():

    # Record start time of simulation for optimization purposes
    start = time.time()

    # Initialize a variable that stores number of times the model was relaxed
    num_relaxation = 0

    # Obtain initial timer settings and cycle time
    u, C, trajectory, relaxed = do_mpc()
    u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
    num_relaxation += relaxed
    step_C = 0

    print(f"u = {u_sorted}")
    print(f"C = {C}")
    print(f"phases = {phases}")

    temp_spawned_katip_s = []
    temp_spawned_katip_n = []
    temp_spawned_aurora_w = []
    temp_spawned_aurora_e = []

    for step in range(sim_duration+1):

        #dummy_delta_step = step-step_C
        
        # Get the average queue time of all incoming roads
        qt_katip_south, qt_katip_north, qt_aurora_west, qt_aurora_east = perf.get_avg_wait()
        
        # Get the average flow rate of all incoming roads
        traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 60)

        #totalcarflow = perf.get_car_flow("all")
    
        # "Snapshot" of vehicles that are stationary (for queue length)
        # Ensures that recorded stationary vehicles belong to the queue
        new_stopped_vehs = perf.get_queue_length(stopped_vehs, 1, step)

        # Obtain cumulative number of vehicles inserted in the simulation since time 0
        spawned_katip_south, spawned_katip_north, spawned_aurora_west, spawned_aurora_east = perf.get_spawned_vehs()
        temp_spawned_katip_s.append(spawned_katip_south)
        temp_spawned_katip_n.append(spawned_katip_north)
        temp_spawned_aurora_w.append(spawned_aurora_west)
        temp_spawned_aurora_e.append(spawned_aurora_east)
    
        # Obtain average queueing time and flow rate of all incoming roads
        if step > 0:
            flow_katip_south = perf.get_flow_rate("KatipS")
            flow_katip_north = perf.get_flow_rate("KatipN")
            flow_aurora_west = perf.get_flow_rate("AuroraW")
            flow_aurora_east = perf.get_flow_rate("AuroraE")
            ql_katip_south, ql_katip_north, ql_aurora_west, ql_aurora_east, new_stopped_vehs = perf.get_queue_length(new_stopped_vehs, 0, step)

        # Record traffic data for each time step except zeroth second
        if step == 0:
            traci.simulationStep()
            continue

        if step > sim_duration:
            print("The simulation has ended!")
            break

        if step%steps_per_s == 0:

            actual_time_step = step//steps_per_s

            delta_step = actual_time_step-step_C

            hr, mins, sec, am_pm = perf.convert_to_real_time(actual_time_step)
            print(f"Timestep: {actual_time_step}")
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

            # Obtain vehicle count in all incoming roads
            n_katip_south, n_katip_north, n_aurora_west, n_aurora_east = perf.get_vehicle_count("all")

            sum_spawned_katip_s = sum(temp_spawned_katip_s)
            sum_spawned_katip_n = sum(temp_spawned_katip_n)
            sum_spawned_aurora_w = sum(temp_spawned_aurora_w)
            sum_spawned_aurora_e = sum(temp_spawned_aurora_e)

            save_sim.write_results_per_sec([n_katip_south, n_katip_north, n_aurora_west, n_aurora_east],
                                [ql_katip_south, ql_katip_north, ql_aurora_west, ql_aurora_east],
                                [qt_katip_south, qt_katip_north, qt_aurora_west, qt_aurora_east], 
                                [flow_katip_south, flow_katip_north, flow_aurora_west, flow_aurora_east],
                                [sum_spawned_katip_s, sum_spawned_katip_n, sum_spawned_aurora_w, sum_spawned_aurora_e],
                                actual_time_step, u_sorted, C)
            
            temp_spawned_katip_s.clear()
            temp_spawned_katip_n.clear()
            temp_spawned_aurora_w.clear()
            temp_spawned_aurora_e.clear()

            # Perform MPC once a control interval has completed
            if delta_step+1 == C:

                print("Performing MPC to compute optimal green times!")
                # Recompute timer settings and cycle time
                u, C, trajectory, relaxed = do_mpc(np.array([n_katip_south, n_katip_north, n_aurora_west_fair, n_aurora_east_fair]), actual_time_step+1)
                u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
                num_relaxation += relaxed

                step_C = actual_time_step+1
            
                print(f"u = {u_sorted}")
                print(f"C = {C}")
                print(f"phases = {phases}")

                save_sim.write_results_per_cycle(actual_time_step, [n_katip_south, n_katip_north, n_aurora_west_fair, n_aurora_east_fair], trajectory)

        # Step the simulation by 1 second
        traci.simulationStep()
        print("\n")

    # Record start time of simulation for profiling purposes
    print(f"Runtime of simulation: {time.time()-start}")
    print(f"Number of times that model was relaxed: {num_relaxation}")

    traci.close()

if __name__ == "__main__":
    main()