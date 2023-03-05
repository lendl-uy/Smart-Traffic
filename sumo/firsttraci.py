import os,sys
if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "C:\\Program Files (x86)\\Eclipse\\Sumo\\bin\\sumo-gui.exe"
#sumoCmd = [sumoBinary, "-c", "C:\Users\EISLER GO\Desktop\thesis sumo\uturn.sumo.cfg"]
sumoCmd = [sumoBinary, "-c", "C:\\Users\\EISLER GO\\Desktop\\thesis sumo\\newnames.sumo.cfg"]

import traci
import traci.constants as tc

traci.start(sumoCmd)



junctionID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'

trafficlightID='cluster9883633497_cluster_25353129_33471551_cluster_26272655_288063291_29500569_5064338396_#2more'



#traci.junction.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

sumcar=0
for step in range(10000):
   print("step", step)
   traci.simulationStep()
   #print(traci.junction.getContextSubscriptionResults(junctionID))
   KatipSl0=traci.lane.getLastStepVehicleNumber('KatipS1_0')+traci.lane.getLastStepVehicleNumber('KatipS2_0')+traci.lane.getLastStepVehicleNumber('KatipS3_0')
   KatipSl1=traci.lane.getLastStepVehicleNumber('KatipS1_1')+traci.lane.getLastStepVehicleNumber('KatipS2_1')+traci.lane.getLastStepVehicleNumber('KatipS3_1')
  # KatipSJ=traci.junction.getLastStepVehicleNumber('KatipJS1')+traci.junction.getLastStepVehicleNumber('KatipJS2')
   KatipSJ=0
   print("Vehicles KatipS: ", KatipSl0+KatipSl1+KatipSJ)
   
   KatipNl0=traci.lane.getLastStepVehicleNumber('KatipN1_0')+traci.lane.getLastStepVehicleNumber('KatipN2_0')+traci.lane.getLastStepVehicleNumber('KatipN3_0')+traci.lane.getLastStepVehicleNumber('KatipN4_0')+traci.lane.getLastStepVehicleNumber('KatipN5_0')
   KatipNl1=traci.lane.getLastStepVehicleNumber('KatipN1_1')+traci.lane.getLastStepVehicleNumber('KatipN2_1')+traci.lane.getLastStepVehicleNumber('KatipN3_1')+traci.lane.getLastStepVehicleNumber('KatipN4_1')+traci.lane.getLastStepVehicleNumber('KatipN5_1')
   #KatipNJ=traci.junction.getLastStepVehicleNumber('KatipJN1')+traci.junction.getLastStepVehicleNumber('KatipJN2')+traci.junction.getLastStepVehicleNumber('KatipJN3')+traci.junction.getLastStepVehicleNumber('KatipJN4')
   KatipNJ=0
   print("Vehicles KatipN: ", KatipNl0+KatipNl1+KatipNJ)
   AuroW=traci.lane.getLastStepVehicleNumber('AuroW_0')+traci.lane.getLastStepVehicleNumber('AuroW_1')+traci.lane.getLastStepVehicleNumber('AuroW_2')+traci.lane.getLastStepVehicleNumber('AuroW_3')
   print("Vehicles AuroW:",AuroW) 
   
   AuroEl0=traci.lane.getLastStepVehicleNumber('AuroE1_0')+traci.lane.getLastStepVehicleNumber('AuroE2_0')+traci.lane.getLastStepVehicleNumber('AuroE3_0')
   AuroEl1=traci.lane.getLastStepVehicleNumber('AuroE1_1')+traci.lane.getLastStepVehicleNumber('AuroE2_1')+traci.lane.getLastStepVehicleNumber('AuroE3_1')
   AuroEl2=traci.lane.getLastStepVehicleNumber('AuroE1_2')+traci.lane.getLastStepVehicleNumber('AuroE2_2')+traci.lane.getLastStepVehicleNumber('AuroE3_2')
   AuroEl3=traci.lane.getLastStepVehicleNumber('AuroE1_3')+traci.lane.getLastStepVehicleNumber('AuroE2_3')+traci.lane.getLastStepVehicleNumber('AuroE3_3')
   AuroEJ=0
   print("Vehicles AuroW:",AuroEl0+AuroEl1+AuroEl2+AuroEl3) 
   #sumcar=sumcar+AuroEl0+AuroEl1+AuroEl2+AuroEl3+AuroW+KatipSl0+KatipSl1+KatipSJ+KatipSl0+KatipSl1+KatipSJ
   
  # print(sumcar)
   if step==100:
     traci.trafficlight.setRedYellowGreenState(trafficlightID, 'gGGgGGGG')
   
   
traci.close()

