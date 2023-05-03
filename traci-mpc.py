# Authors: Eisler Spencer Go, Jan Lendl R. Uy
# Interfacing of SUMO simulation via TraCI

import os
import sys
import time

import traci
import traci.constants as tc
import numpy as np

#from mpc_params import *
from mpc import *

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

    arrived_veh_ids = []

    list_of_ql_15_window = [0.0]
    ql_15min = 0

    list_of_qt_15_window = [0.0]
    departed_vehs_qt = 0

    list_of_flow_15_window = [0.0]
    departed_vehs_flow = 0

    for step in range(sim_steps+1):

        # Record traffic data for each time step except zeroth second
        if step == 0:
            traci.simulationStep()
            continue

        if step > sim_steps:
            break
        
        # Initialize the measurement of average flow rate of all incoming roads
        traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 60)
    
        # "Snapshot" of vehicles that are stationary (for queue length)
        # Ensures that recorded stationary vehicles belong to the queue
        new_stopped_vehs = perf.sample_queue_length(stopped_vehs, 1, step)

        # Sample and update the running windowed average values of performance indicators
        perf.sample_queue_time(step)
        perf.sample_flow_rate(step)
        temp_list_queue_times, arrived_veh_ids = perf.update_windowed_queue_time(arrived_veh_ids, departed_vehs_qt)
        departed_vehs_flow = perf.update_windowed_flow_rate(departed_vehs_flow)
        ql_15min, new_stopped_vehs = perf.sample_queue_length(new_stopped_vehs, 0, step, ql_15min) # Get the average queue length from the past 15 mins

        # Obtain the 15-minute windowed average of the performance indicators
        if step % sampling_time == 0:

            # Get the windowed average queue length
            ql_15min_final, ql_15min = perf.get_windowed_queue_length(ql_15min)
            list_of_ql_15_window.append(ql_15min_final)
            #print("List of average queue lengths for 15 min windows", list_of_ql_15_window)

            # Get the windowed average flow rate
            flow_15min, departed_vehs_flow = perf.get_windowed_flow_rate(departed_vehs_flow)
            list_of_flow_15_window.append(flow_15min)
            #print("List of average flow rates for 15 min windows", list_of_flow_15_window)

            # Get the windowed average queue time
            qt_15min, departed_vehs_qt = perf.get_windowed_queue_time(temp_list_queue_times, departed_vehs_qt, arrived_veh_ids)
            list_of_qt_15_window.append(qt_15min)
            #print(f"List of average queue time for 15 min windows: {list_of_qt_15_window}")

        if step % steps_per_s == 0:

            actual_time_step = step//steps_per_s

            delta_step = actual_time_step-step_C

            hr, mins, sec, am_pm = perf.convert_to_real_time(actual_time_step)
            print(f"Timestep: {actual_time_step}")
            print(f"Current time step relative to new phase: {delta_step}")
            print(f"{hr}:{mins}:{sec} {am_pm}")

            # Perform switching of phases based on the current time step
            # Adjusts timer settings of all stoplights based on computed green times
            if delta_step == 0:
                traci.trafficlight.setPhase(trafficlightID, 0)
                traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[0])
                print(f"Timer applied: {u_sorted[0]} s")
            elif delta_step == phases[1]-3:
                traci.trafficlight.setPhase(trafficlightID, 1)
                traci.trafficlight.setPhaseDuration(trafficlightID, 3)
                print(f"Timer applied: 3 s")
            elif delta_step == phases[1]:
                #traci.trafficlight.setPhase(trafficlightID, 2)
                #traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[3])
                # Handle skipping of phase 2
                if phase_2_skipped(phases):
                    print("Phase 2 was skipped!")
                    traci.trafficlight.setPhase(trafficlightID, 4)
                    traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[2])
                    n_aurora_west_fair = n_aurora_west # Save vehicle count for Aurora West (just before green time)
                else:
                    traci.trafficlight.setPhase(trafficlightID, 2)
                    traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[3])
                n_aurora_east_fair = n_aurora_east # Save vehicle count for Aurora East (just before green time)
                n_aurora_east_lane4_fair = n_aurora_east_lane4 # Save vehicle count of Aurora East Lane 4 (just before green time)
                print(f"Timer applied: {u_sorted[3]} s")
            elif delta_step == phases[2]-3:
                # Do nothing if phase 2 is skipped
                if not phase_2_skipped(phases):
                    traci.trafficlight.setPhase(trafficlightID, 3)
                    traci.trafficlight.setPhaseDuration(trafficlightID, 3)
                    print(f"Timer applied: 3 s")
            elif delta_step == phases[2]:
                # Do nothing if phase 2 is skipped
                if not phase_2_skipped(phases):
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
            n_katip_south, n_katip_north, n_aurora_west, n_aurora_east, n_aurora_east_lane4 = perf.get_vehicle_count("all")

            save_sim.write_results_per_sec([n_katip_south, n_katip_north, n_aurora_west, n_aurora_east],
                                            actual_time_step, u_sorted, C)
            
            if step % sampling_time == 0:
                save_sim.write_results_per_window(ql_15min_final, qt_15min, flow_15min, actual_time_step)
            
            # Perform MPC once a control interval has completed
            if delta_step+1 == C:

                print("Performing MPC to compute optimal green times!")
                # Recompute timer settings and cycle time
                if actual_time_step+N*C < sim_duration:
                    u, C, trajectory, relaxed = do_mpc(np.array([n_katip_south, n_katip_north, n_aurora_west_fair, n_aurora_east_fair, n_aurora_east_lane4_fair]), 
                                                    actual_time_step+1)
                    if u != None:
                        u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
                        num_relaxation += relaxed

                step_C = actual_time_step+1

                save_sim.write_results_per_cycle(actual_time_step, trajectory)
            
                print(f"u = {u_sorted}")
                print(f"C = {C}")
                print(f"phases = {phases}")
          
        if step == sim_steps:
            final_ql = perf.get_cumulative_queue_length()
            final_qt = perf.get_cumulative_queue_time()
            final_flow = perf.get_cumulative_flow_rate()
            save_sim.write_final_results(final_ql, final_qt, final_flow, actual_time_step)
        
        # Step the simulation by 1 second
        traci.simulationStep()
        print("\n")

    # Record start time of simulation for profiling purposes
    print(f"Runtime of simulation: {time.time()-start}")
    print(f"Number of times that model was relaxed: {num_relaxation}")

    traci.close()
    sys.exit("The simulation has ended!")

if __name__ == "__main__":
    main()