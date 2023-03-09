# Authors: Eisler Spencer Go, Jan Lendl R. Uy
# Interfacing of SUMO simulation via TraCI

# Conventions
# KatipS: Katipunan Southbound / Katipunan North
# KatipN: Katipunan Northbound / Katipunan South
# AuroW: Aurora Westbound / Aurora East
# AuroE: Aurora Eastbound / Aurora West

import os
import sys
import traci
import traci.constants as tc
import numpy as np

from mpc_params import *
from mpc import *

def convert_to_real_time(step):
    hr = step//3600
    mins = (step//60)%60
    sec = step%60

    hr += 6
    if hr >= 12:
        am_pm = "PM"
    else:
        am_pm = "AM"

    if hr < 10:
        hr = "0"+str(hr)
    
    if mins < 10:
        mins = "0"+str(mins)

    if sec < 10:
        sec = "0"+str(sec)

    return hr, mins, sec, am_pm
     
# Declaration of environment variable
if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")

# Directory of sumo-gui and sumocfg files
sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
sumoCmd = [sumoBinary, "-c", "C:\\Users\\lendl\\OneDrive\\Documents\\smart_traffic\\sumo\\4-3-test-demand.sumocfg"]

# Starts the simulation
traci.start(sumoCmd)

# Junction IDs and Traffic Light IDs
junctionID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'
trafficlightID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'

#traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

# Actual simulation
# Entire simulation spans from 6AM to 8PM traffic (14 hrs/50400 secs)
# 1 step corresponds to 1 second

sim_duration = 50400

# Obtain initial timer settings and cycle time
u, C = do_mpc()
u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
step_C = 0

print(f"u = {u_sorted}")
print(f"C = {C}")
print(f"phases = {phases}")

sumcar = 0
for step in range(sim_duration):

    hr, mins, sec, am_pm = convert_to_real_time(step)
    print(f"Timestep: {step}")
    print(f"{hr}:{mins}:{sec} {am_pm}")

    delta_step = step-step_C

    # Perform switching of phases based on the current time step
    # Adjusts timer settings of all stoplights based on computed green times
    if delta_step == 0:
        traci.trafficlight.setPhase(trafficlightID, 0)
        traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[0])
    elif delta_step == phases[1]-3:
        traci.trafficlight.setPhase(trafficlightID, 1)
        traci.trafficlight.setPhaseDuration(trafficlightID, 3)
    elif delta_step == phases[1]:
        traci.trafficlight.setPhase(trafficlightID, 2)
        traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[3])
    elif delta_step == phases[2]-3:
        traci.trafficlight.setPhase(trafficlightID, 3)
        traci.trafficlight.setPhaseDuration(trafficlightID, 3)
    elif delta_step == phases[2]:
        traci.trafficlight.setPhase(trafficlightID, 4)
        traci.trafficlight.setPhaseDuration(trafficlightID, u_sorted[2])
    elif delta_step == C-3:
        traci.trafficlight.setPhase(trafficlightID, 5)
        traci.trafficlight.setPhaseDuration(trafficlightID, 3)

    # Step the simulation by 1 second
    traci.simulationStep()

    print(f"Current phase number: {traci.trafficlight.getPhase(trafficlightID)}")
    print(f"Current time step relative to new phase: {delta_step}")

    # Obtain vehicle count in Katipunan North
    #print(traci.junction.getContextSubscriptionResults(junctionID))
    KatipSl0=traci.lane.getLastStepVehicleNumber('1076383725.80_0')+traci.lane.getLastStepVehicleNumber('1076383725.44_0')+traci.lane.getLastStepVehicleNumber('1076383725_0')
    KatipSl1=traci.lane.getLastStepVehicleNumber('1076383725.80_1')+traci.lane.getLastStepVehicleNumber('1076383725.44_1')+traci.lane.getLastStepVehicleNumber('1076383725_1')
    # KatipSJ=traci.junction.getLastStepVehicleNumber('KatipJS1')+traci.junction.getLastStepVehicleNumber('KatipJS2')
    KatipSJ=0
    #print("Vehicles KatipS: ", KatipSl0+KatipSl1+KatipSJ)
    katip_north = KatipSl0+KatipSl1
    print("Vehicles in Katipunan North: ", KatipSl0+KatipSl1)
    
    # Obtain vehicle count in Katipunan South
    KatipNl0=traci.lane.getLastStepVehicleNumber('780157087#2_2')+traci.lane.getLastStepVehicleNumber('780157087#0.33_0')+traci.lane.getLastStepVehicleNumber('780157087#0.14_0')+traci.lane.getLastStepVehicleNumber('780157087#0_0')+traci.lane.getLastStepVehicleNumber('1078018163_0')
    KatipNl1=traci.lane.getLastStepVehicleNumber('780157087#2_1')+traci.lane.getLastStepVehicleNumber('780157087#0.33_1')+traci.lane.getLastStepVehicleNumber('780157087#0.14_1')+traci.lane.getLastStepVehicleNumber('780157087#0_1')+traci.lane.getLastStepVehicleNumber('1078018163_1')
    #KatipNJ=traci.junction.getLastStepVehicleNumber('KatipJN1')+traci.junction.getLastStepVehicleNumber('KatipJN2')+traci.junction.getLastStepVehicleNumber('KatipJN3')+traci.junction.getLastStepVehicleNumber('KatipJN4')
    KatipNJ=0
    #print("Vehicles KatipN: ", KatipNl0+KatipNl1+KatipNJ)
    katip_south = KatipNl0+KatipNl1
    print("Vehicles in Katipunan South: ", KatipNl0+KatipNl1)

    # Obtain vehicle count in Aurora East
    AuroW=traci.lane.getLastStepVehicleNumber('933952934#0_0')+traci.lane.getLastStepVehicleNumber('933952934#0_1')+traci.lane.getLastStepVehicleNumber('933952934#0_2')+traci.lane.getLastStepVehicleNumber('933952934#0_3')
    #AuroW=traci.lane.getLastStepVehicleNumber('933952934#0_0')
    aurora_east = AuroW
    print("Vehicles in Aurora East:",AuroW) 
    
    # Obtain vehicle count in Aurora West
    AuroEl0=traci.lane.getLastStepVehicleNumber('591107291#0_0')+traci.lane.getLastStepVehicleNumber('591107291#1_0')+traci.lane.getLastStepVehicleNumber('609205085_0')
    AuroEl1=traci.lane.getLastStepVehicleNumber('591107291#0_1')+traci.lane.getLastStepVehicleNumber('591107291#1_1')+traci.lane.getLastStepVehicleNumber('609205085_1')
    AuroEl2=traci.lane.getLastStepVehicleNumber('591107291#0_2')+traci.lane.getLastStepVehicleNumber('591107291#1_2')+traci.lane.getLastStepVehicleNumber('609205085_2')
    AuroEl3=traci.lane.getLastStepVehicleNumber('591107291#0_3')+traci.lane.getLastStepVehicleNumber('591107291#1_3')+traci.lane.getLastStepVehicleNumber('609205085_3')
    #AuroEJ=0
    #print("Vehicles AuroW:",AuroEl0+AuroEl1+AuroEl2+AuroEl3)
    aurora_west = AuroEl0+AuroEl1+AuroEl2+AuroEl3
    print("Vehicles in Aurora West:",AuroEl0+AuroEl1+AuroEl2+AuroEl3) 
    #sumcar=sumcar+AuroEl0+AuroEl1+AuroEl2+AuroEl3+AuroW+KatipSl0+KatipSl1+KatipSJ+KatipSl0+KatipSl1+KatipSJ
    
    # print(sumcar)
    # Perform MPC once a control interval has completed
    if delta_step+1 == C:
        # Recompute timer settings and cycle time
        u, C = do_mpc(np.array([katip_south, katip_north, aurora_west, aurora_east]), step+1)
        u_sorted, phases = get_timer_settings(u, C) # Retrieves parsed timer setting information
        step_C = step
     
        print(f"u = {u_sorted}")
        print(f"C = {C}")
        print(f"phases = {phases}")

traci.close()
