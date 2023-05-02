# Authors: Eisler Spencer Go, Jan Lendl R. Uy
# Interfacing of SUMO simulation via TraCI

import os
import sys
import time
import copy

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
    sys.exit("Please declare environment variable 'SUMO_HOME'!")

# Directory of sumo-gui and sumocfg files
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:\\Users\\Lendl\\Documents\\smart_traffic\\sumo\\micro\\003\\iteration_003.sumocfg"]

# Starts the simulation
traci.start(sumoCmd)

# Junction IDs and Traffic Light IDs
junctionID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'
trafficlightID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'

step_len = 0.5
steps_per_s = int(1/step_len)
sim_duration = 50400
sim_steps = int(50400/step_len) # Fixed

meas_15min_window = 15*60 # 15 minutes -> 900 seconds
sampling_time = int(meas_15min_window/step_len)

allcar={}
stopped_vehs = {}
averagewaitlist={}

n_aurora_west = 0
n_aurora_east = 0

# Actual simulation
# Entire simulation spans from 6AM to 8PM traffic (14 hrs/50400 secs)
# 1 step corresponds to 0.5 seconds

def main():

    # Record start time of simulation for optimization purposes
    start = time.time()

    step_C = 0

    # Initialize a variable that stores number of times the model was relaxed

    arrived_veh_ids = []

    list_of_ql_15_window = [0.0]
    ql_15min = 0

    list_of_qt_15_window = [0.0]

    list_of_flow_15_window = [0.0]
    departed_vehs = 0

    for step in range(sim_steps+1):

        # Record traffic data for each time step except zeroth second
        if step == 0:
            traci.simulationStep()
            continue

        if step > sim_steps:
            break
        
        # Get the average queue time of all incoming roads
        perf.get_queue_time(step)
        
        # Initialize the measurement of average flow rate of all incoming roads
        traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 60)
    
        # "Snapshot" of vehicles that are stationary (for queue length)
        # Ensures that recorded stationary vehicles belong to the queue
        new_stopped_vehs = perf.get_queue_length(stopped_vehs, 1, step)

        temp_list_queue_times = perf.get_windowed_queue_time(arrived_veh_ids, departed_vehs)

        # Measure the temporary values of performance indicators for each time step
        if step < sim_steps:
            ql_15min_final, ql_15min, new_stopped_vehs = perf.get_queue_length(new_stopped_vehs, 0, step, ql_15min) # Get the average queue length from the past 15 mins
            flow_katip_south = perf.get_flow_rate("KatipS")
            flow_katip_north = perf.get_flow_rate("KatipN")
            flow_aurora_west = perf.get_flow_rate("AuroraW")
            flow_aurora_east = perf.get_flow_rate("AuroraE")
            flow_all_roads = perf.get_flow_rate("all")
        # Obtain the final cumulative averages of the performance indicators
        else:
            ql_15min_final, ql_15min, final_ql = perf.get_queue_length(new_stopped_vehs, 0, step, ql_15min) # Get the cumulative average queue length
            final_qt = perf.get_queue_time(step)
            flow_katip_south = perf.get_flow_rate("KatipS")
            flow_katip_north = perf.get_flow_rate("KatipN")
            flow_aurora_west = perf.get_flow_rate("AuroraW")
            flow_aurora_east = perf.get_flow_rate("AuroraE")
            flow_all_roads = perf.get_flow_rate("all")
        
        # Obtain the 15-minute windowed average of the performance indicators
        if step % sampling_time == 0:

            # Get the windowed average queue length
            list_of_ql_15_window.append(ql_15min_final)
            ql_15min = 0
            #print("List of average queue lengths for 15 min windows", list_of_ql_15_window)

            # Get the windowed average flow rate
            flow_15min = (departed_vehs/1800)*3600
            list_of_flow_15_window.append(flow_15min)
            departed_vehs = 0
            #print("List of average flow rates for 15 min windows", list_of_flow_15_window)

            # Get the windowed average queue time
            qt_15min = sum(temp_list_queue_times.values())/len(temp_list_queue_times)
            list_of_qt_15_window.append(qt_15min)
            #print(f"List of average queue time for 15 min windows: {list_of_qt_15_window}")
            for i in range(len(arrived_veh_ids)):
                temp_list_queue_times.pop(arrived_veh_ids[i],None)

        if step % steps_per_s == 0:

            actual_time_step = step//steps_per_s

            delta_step = actual_time_step-step_C

            hr, mins, sec, am_pm = perf.convert_to_real_time(actual_time_step)
            print(f"Timestep: {actual_time_step}")
            print(f"Current time step relative to new phase: {delta_step}")
            print(f"{hr}:{mins}:{sec} {am_pm}")

            phase_num = traci.trafficlight.getPhase(trafficlightID)

            print(f"Current phase number: {phase_num}")

            # Obtain vehicle count in all incoming roads
            n_katip_south, n_katip_north, n_aurora_west, n_aurora_east, n_aurora_east_lane4 = perf.get_vehicle_count("all")

            save_sim.write_results_per_sec([n_katip_south, n_katip_north, n_aurora_west, n_aurora_east],
                                            actual_time_step)
            
            # Perform MPC once a control interval has completed
            if delta_step+1 == 154:
                step_C = actual_time_step+1

            if step % sampling_time == 0:
                save_sim.write_results_per_window(ql_15min_final, qt_15min, flow_15min, actual_time_step)
          
        if step == sim_steps:
            save_sim.write_final_results(final_ql, final_qt, [flow_katip_south, flow_katip_north, flow_aurora_west, flow_aurora_east, flow_all_roads], actual_time_step)
        
        # Step the simulation by 1 second
        traci.simulationStep()
        print("\n")

    # Record start time of simulation for profiling purposes
    print(f"Runtime of simulation: {time.time()-start}")

    traci.close()
    sys.exit("The simulation has ended!")

if __name__ == "__main__":
    main()