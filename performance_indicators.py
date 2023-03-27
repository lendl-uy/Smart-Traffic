# -*- coding: utf-8 -*-
"""
Performance Indicators
Created on Sat Mar 11 11:09:29 2023

@author: franc
"""
	 
import traci
import traci.constants as tc
import numpy as np

from mpc_params import *
from mpc import *
from road_defs import *

# Global variables
global averagewaitlist
averagewaitlist={}

global keyofkey
keyofkey=0

averagewaitlist_katip_s = {}
averagewaitlist_katip_n = {}
averagewaitlist_aurora_w = {}
averagewaitlist_aurora_e = {}

avlenKs=[]
avlenKn=[]
avlenAe=[]
avlenAw=[]

KatipN_edge_ids_persistent = []
KatipS_edge_ids_persistent = []
AuroraW_edge_ids_persistent = []
AuroraE_edge_ids_persistent = []

spawned_katip_s = []
spawned_katip_n = []
spawned_aurora_w = []
spawned_aurora_e = []

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

def get_vehicle_count(road_name):

    road_names = ["KatipN", "KatipS", "AuroraW", "AuroraE", "all"]

    # Error handling
    if road_name not in road_names:
        print("Invalid road name. Valid road names are: [KatipN, KatipS, AuroraW, AuroraE, all]")
        return 0
        
    # Obtain vehicle count in KatipN
    if road_name == "KatipN":
        # List of edges in KatipS
        KatipN_edge_list = ['1076383725', '1076383725.44', '1076383725.80']
        KatipN_edge_ids = []

        # Add the list vehicle IDs on each edge to a single list
        for _edge in KatipN_edge_list:
            KatipN_edge_ids += traci.edge.getLastStepVehicleIDs(_edge)
        
        # List of junctions in KatipN
        KatipN_junction_list = ['J2', 'J0']
        KatipN_junction_ids = []
        # Add the list vehicle IDs on each junction to a single list
        for _junction in KatipN_junction_list:
            traci.junction.subscribeContext(_junction, tc.CMD_GET_VEHICLE_VARIABLE, 10)
            KatipN_junction_ids += list(traci.junction.getContextSubscriptionResults(_junction).keys())
        
        # Combine both vehicle ID lists into a set, removing duplicates
        KatipN_combined_ids = set(KatipN_junction_ids + KatipN_edge_ids)

        # The length of this set gives the total number of cars in KatipN
        KatipN_total = len(KatipN_combined_ids)
        print("Vehicles in KatipN: ", KatipN_total)
        return KatipN_total
    
    # Obtain vehicle count in KatipS
    elif road_name == "KatipS":
        # List of edges in KatipS
        KatipS_edge_list = ['1078018163', '780157087#2', '780157087#0.33', '780157087#0.14', '780157087#0']
        KatipS_edge_ids = []

        # Add the list vehicle IDs on each edge to a single list
        for _edge in KatipS_edge_list:
            KatipS_edge_ids += traci.edge.getLastStepVehicleIDs(_edge)
        
        # List of junctions in KatipS
        KatipS_junction_list = ['9883633498', '1020313312', 'J5', 'J7']
        KatipS_junction_ids = []
        # Add the list vehicle IDs on each junction to a single list
        for _junction in KatipS_junction_list:
            traci.junction.subscribeContext(_junction, tc.CMD_GET_VEHICLE_VARIABLE, 10)
            KatipS_junction_ids += list(traci.junction.getContextSubscriptionResults(_junction).keys())
        
        # Combine both vehicle ID lists into a set, removing duplicates
        KatipS_combined_ids = set(KatipS_junction_ids + KatipS_edge_ids)

        # The length of this set gives the total number of cars in KatipS
        KatipS_total = len(KatipS_combined_ids)
        print("Vehicles in KatipS: ", KatipS_total)
        return KatipS_total

    # Obtain vehicle count in AuroraE
    elif road_name == "AuroraE":
        # List of edges in AuroraE
        AuroraE_edge_list = ['933952934#0']
        AuroraE_edge_ids = []

        # Add the list vehicle IDs on each edge to a single list
        for _edge in AuroraE_edge_list:
            AuroraE_edge_ids += traci.edge.getLastStepVehicleIDs(_edge)
        
        # List of junctions in AuroraE
        AuroraE_junction_list = []
        AuroraE_junction_ids = []
        # Add the list vehicle IDs on each junction to a single list
        for _junction in AuroraE_junction_list:
            traci.junction.subscribeContext(_junction, tc.CMD_GET_VEHICLE_VARIABLE, 10)
            AuroraE_junction_ids += list(traci.junction.getContextSubscriptionResults(_junction).keys())
        
        # Combine both vehicle ID lists into a set, removing duplicates
        AuroraE_combined_ids = set(AuroraE_junction_ids + AuroraE_edge_ids)

        # The length of this set gives the total number of cars in AuroraE
        AuroraE_total = len(AuroraE_combined_ids)
        print("Vehicles in AuroraE: ", AuroraE_total)
        return AuroraE_total

    # Obtain vehicle count in AuroraW
    elif road_name == "AuroraW":
        # List of edges in AuroraW
        AuroraW_edge_list = ['609205085', '591107291#1', '591107291#0']
        AuroraW_edge_ids = []

        # Add the list vehicle IDs on each edge to a single list
        for _edge in AuroraW_edge_list:
            AuroraW_edge_ids += traci.edge.getLastStepVehicleIDs(_edge)
        
        # List of junctions in AuroraW
        AuroraW_junction_list = ['288063295', '6565591286']
        AuroraW_junction_ids = []
        # Add the list vehicle IDs on each junction to a single list
        for _junction in AuroraW_junction_list:
            traci.junction.subscribeContext(_junction, tc.CMD_GET_VEHICLE_VARIABLE, 10)
            AuroraW_junction_ids += list(traci.junction.getContextSubscriptionResults(_junction).keys())
        
        # Combine both vehicle ID lists into a set, removing duplicates
        AuroraW_combined_ids = set(AuroraW_junction_ids + AuroraW_edge_ids)

        # The length of this set gives the total number of cars in AuroraW
        AuroraW_total = len(AuroraW_combined_ids)
        print("Vehicles in AuroraW: ", AuroraW_total)
        return AuroraW_total
    
    elif road_name == "all":
        KatipS_total = get_vehicle_count("KatipS")
        KatipN_total = get_vehicle_count("KatipN")
        AuroraE_total = get_vehicle_count("AuroraE")
        AuroraW_total = get_vehicle_count("AuroraW")
        all_roads = KatipS_total, KatipN_total, AuroraW_total, AuroraE_total
        return all_roads

def get_queue_length(record_stopped_vehs, record, step):

    # Obtains all the vehicle IDs in the simulation
    sim_vehicles = traci.vehicle.getIDList()

    # Record vehicle IDs of nonmoving vehicles to filter out 
    # incorrectly assumed queued vehicles
    if record == 1:
        # Record stationary vehicles
        to_remove = []
        for veh in sim_vehicles:
            if traci.vehicle.getSpeed(veh) == 0.0:
                if veh not in record_stopped_vehs.keys():
                    record_stopped_vehs[veh] = [1,step]
                elif record_stopped_vehs[veh][1] == step-1:
                    record_stopped_vehs[veh][0] = record_stopped_vehs[veh][0]+1 # Increment occurrence
                    record_stopped_vehs[veh][1] = step # Increment occurrence
                else:
                    to_remove.append(veh)
            else:
                if veh in record_stopped_vehs.keys():
                    to_remove.append(veh)
        # Remove redundant records of stationary vehicles that have 
        # already left simulation
        for veh in record_stopped_vehs:
            if veh not in sim_vehicles:
                to_remove.append(veh)
        for i in range(len(to_remove)):
            record_stopped_vehs.pop(to_remove[i])
        return record_stopped_vehs

    # Meant to serve as filter for vehicles that stop not as an effect of stoplights

    ql_katip_south_lane_1 = []
    ql_katip_south_lane_2 = []
    ql_katip_north_lane_1 = []
    ql_katip_north_lane_2 = []
    ql_aurora_west_lane_1 = []
    ql_aurora_west_lane_2 = []
    ql_aurora_west_lane_3 = []
    ql_aurora_west_lane_4 = []
    ql_aurora_east_lane_1 = []
    ql_aurora_east_lane_2 = []
    ql_aurora_east_lane_3 = []
    ql_aurora_east_lane_4 = []

    avg_ql_katip_south = 0.0
    avg_ql_katip_north = 0.0
    avg_ql_aurora_west = 0.0
    avg_ql_aurora_east = 0.0

    # Check if nonmoving vehicle was also at stop 3 steps ago
    # Ensures that recorded stationary vehicles belong to the queue
    if record == 0:

        for veh in record_stopped_vehs.keys():
            if record_stopped_vehs[veh][0] >= 3:

                lane_id = traci.vehicle.getLaneID(veh)
                veh_len = traci.vehicle.getLength(veh)

                # Append length of all stationary vehicles in respective lsits
                if lane_id in katip_south_edges:
                    if lane_id in katip_south_lane_1:
                        ql_katip_south_lane_1.append(veh_len)
                    elif lane_id in katip_south_lane_2:
                        ql_katip_south_lane_2.append(veh_len)
                elif lane_id in katip_north_edges:
                    if lane_id in katip_north_lane_1:
                        ql_katip_north_lane_1.append(veh_len)
                    elif lane_id in katip_north_lane_2:
                        ql_katip_north_lane_2.append(veh_len)
                elif lane_id in aurora_west_edges:
                    if lane_id in aurora_west_lane_1:
                        ql_aurora_west_lane_1.append(veh_len)
                    elif lane_id in aurora_west_lane_2:
                        ql_aurora_west_lane_2.append(veh_len)
                    elif lane_id in aurora_west_lane_3:
                        ql_aurora_west_lane_3.append(veh_len)
                    elif lane_id in aurora_west_lane_4:
                        ql_aurora_west_lane_4.append(veh_len)
                elif lane_id in aurora_east_edges:
                    if lane_id in aurora_east_lane_1:
                        ql_aurora_east_lane_1.append(veh_len)
                    elif lane_id in aurora_east_lane_2:
                        ql_aurora_east_lane_2.append(veh_len)
                    elif lane_id in aurora_east_lane_3:
                        ql_aurora_east_lane_3.append(veh_len)
                    elif lane_id in aurora_east_lane_4:
                        ql_aurora_east_lane_4.append(veh_len)

        # Obtain the average queue length of all incoming road links
        if len(ql_katip_south_lane_1) != 0:
            avg_ql_katip_south += sum(ql_katip_south_lane_1)
        if len(ql_katip_south_lane_2) != 0:
            avg_ql_katip_south += sum(ql_katip_south_lane_2)
        avg_ql_katip_south /= 2
        
        avlenKs.append(avg_ql_katip_south)  

        if len(ql_katip_north_lane_1) != 0:
            avg_ql_katip_north += sum(ql_katip_north_lane_1)
        if len(ql_katip_north_lane_2) != 0:
            avg_ql_katip_north += sum(ql_katip_north_lane_2)
        avg_ql_katip_north /= 2
        
        avlenKn.append(avg_ql_katip_north)

        if len(ql_aurora_west_lane_1) != 0:
            avg_ql_aurora_west += sum(ql_aurora_west_lane_1)
        if len(ql_aurora_west_lane_2) != 0:
            avg_ql_aurora_west += sum(ql_aurora_west_lane_2)
        if len(ql_aurora_west_lane_3) != 0:
            avg_ql_aurora_west += sum(ql_aurora_west_lane_3)
        if len(ql_aurora_west_lane_4) != 0:
            avg_ql_aurora_west += sum(ql_aurora_west_lane_4)
        avg_ql_aurora_west /= 4
        
        avlenAw.append(avg_ql_aurora_west)

        if len(ql_aurora_east_lane_1) != 0:
            avg_ql_aurora_east += sum(ql_aurora_east_lane_1)
        if len(ql_aurora_east_lane_2) != 0:
            avg_ql_aurora_east += sum(ql_aurora_east_lane_2)
        if len(ql_aurora_east_lane_3) != 0:
            avg_ql_aurora_east += sum(ql_aurora_east_lane_3)
        if len(ql_aurora_east_lane_4) != 0:
            avg_ql_aurora_east += sum(ql_aurora_east_lane_4)
        avg_ql_aurora_east /= 4
        
        avlenAe.append(avg_ql_aurora_east)
        
        Overall_avlenKs=sum(avlenKs)/len(avlenKs)    
        Overall_avlenKn=sum(avlenKn)/len(avlenKn)
        Overall_avlenAe=sum(avlenAe)/len(avlenAe)
        Overall_avlenAw=sum(avlenAw)/len(avlenAw)

        print(f"Average queue length in Katipunan South: {avg_ql_katip_south} m")
        print(f"Average queue length in Katipunan North: {avg_ql_katip_north} m")
        print(f"Average queue length in Aurora West: {avg_ql_aurora_west} m")
        print(f"Average queue length in Aurora East: {avg_ql_aurora_east} m")
        print(f"Overall average queue length in Katipunan South: {Overall_avlenKs} m")
        print(f"Overall average queue length in Katipunan North: {Overall_avlenKn} m")
        print(f"Overall average queue length in Aurora West: {Overall_avlenAw} m")
        print(f"Overall average queue length in Aurora East: {Overall_avlenAe} m")

    return avg_ql_katip_south, avg_ql_katip_north, avg_ql_aurora_west, avg_ql_aurora_east, record_stopped_vehs


def get_car_flow(road_name):
    
    global KatipN_edge_ids_persistent
    global KatipS_edge_ids_persistent
    global AuroraW_edge_ids_persistent
    global AuroraE_edge_ids_persistent

    road_names = ["KatipN", "KatipS", "AuroraW", "AuroraE", "all"]
    # Error handling
    if road_name not in road_names:
        print("Invalid road name. Valid road names are: [KatipN, KatipS, AuroraW, AuroraE, all]")
        return 0

    if road_name == "KatipN":
        KatipN_edge_ids_persistent += traci.edge.getLastStepVehicleIDs('1076383725.80')
        KatipN_edge_ids_persistent = set(KatipN_edge_ids_persistent)
        KatipN_unique_vehicle_count = len(KatipN_edge_ids_persistent)
        KatipN_edge_ids_persistent = list(KatipN_edge_ids_persistent)
        return KatipN_unique_vehicle_count
    
    elif road_name == "KatipS":
        KatipS_edge_ids_persistent += traci.edge.getLastStepVehicleIDs('780157087#2')
        KatipS_edge_ids_persistent = set(KatipS_edge_ids_persistent)
        KatipS_unique_vehicle_count = len(KatipS_edge_ids_persistent)
        KatipS_edge_ids_persistent = list(KatipS_edge_ids_persistent)
        return KatipS_unique_vehicle_count

    elif road_name == "AuroraE":
        AuroraE_edge_ids_persistent += traci.edge.getLastStepVehicleIDs('933952934#0')
        AuroraE_edge_ids_persistent = set(AuroraE_edge_ids_persistent)
        AuroraE_unique_vehicle_count = len(AuroraE_edge_ids_persistent)
        AuroraE_edge_ids_persistent = list(AuroraE_edge_ids_persistent)
        return AuroraE_unique_vehicle_count
    
    elif road_name == "AuroraW":
        AuroraW_edge_ids_persistent += traci.edge.getLastStepVehicleIDs('591107291#1')
        AuroraW_edge_ids_persistent = set(AuroraW_edge_ids_persistent)
        AuroraW_unique_vehicle_count = len(AuroraW_edge_ids_persistent)
        AuroraW_edge_ids_persistent = list(AuroraW_edge_ids_persistent)
        return AuroraW_unique_vehicle_count
    
    elif road_name == "all":
        KatipS = get_car_flow("KatipS")
        KatipN = get_car_flow("KatipN")
        AuroraW = get_car_flow("AuroraW")
        AuroraE = get_car_flow("AuroraE")
        all_road = KatipS + KatipN + AuroraW + AuroraE
        return all_road

def get_flow_rate(road_name):

    step = traci.simulation.getTime()
    road_names = ["KatipN", "KatipS", "AuroraW", "AuroraE", "all"]

    # Error handling
    if road_name not in road_names:
        print("Invalid road name. Valid road names are: [KatipN, KatipS, AuroraW, AuroraE, all]")
        return 0
    
    total_flow = get_car_flow(road_name)
    flow_rate=0

    if step>0:
        flow_rate = total_flow*3600/step

    print(f"Average flow rate in {road_name}: {flow_rate} veh/hr")

    return flow_rate

def get_avg_wait():

    #get averagewaitingtime of current time step 
    global keyofkey

    for veh_id in traci.simulation.getDepartedIDList():
        traci.vehicle.subscribe(veh_id, [tc.VAR_ACCUMULATED_WAITING_TIME])
    
    #keyofkey is needed to fix formatting of output
    if len(list(traci.vehicle.getAllSubscriptionResults().keys()))>0:
        keyofkey=list(traci.vehicle.getAllSubscriptionResults()[(list(traci.vehicle.getAllSubscriptionResults().keys())[0])].keys())[0]
      
    #append new vehicle id with waiting time or update waiting time 
    if keyofkey!=0:
      
        for i in range(len(traci.vehicle.getAllSubscriptionResults())):
            averagewaitlist[list(traci.vehicle.getAllSubscriptionResults().keys())[i]]=traci.vehicle.getAllSubscriptionResults()[list(traci.vehicle.getAllSubscriptionResults().keys())[i]][keyofkey]

        for veh_id in traci.vehicle.getIDList():
            lane_id = traci.vehicle.getLaneID(veh_id)    
          
            if lane_id in katip_south_edges:
                averagewaitlist_katip_s[veh_id] = averagewaitlist[veh_id]
            elif lane_id in katip_north_edges:
                averagewaitlist_katip_n[veh_id] = averagewaitlist[veh_id]
            elif lane_id in aurora_west_edges:
                averagewaitlist_aurora_w[veh_id] = averagewaitlist[veh_id]
            elif lane_id in aurora_east_edges:
                averagewaitlist_aurora_e[veh_id] = averagewaitlist[veh_id]

    if len(averagewaitlist_katip_s)>0:
        avgwt_katip_s = sum(averagewaitlist_katip_s.values()) / float(len(averagewaitlist_katip_s))
    else:
        avgwt_katip_s = 0.0

    if len(averagewaitlist_katip_n)>0:
        avgwt_katip_n = sum(averagewaitlist_katip_n.values()) / float(len(averagewaitlist_katip_n))
    else:
        avgwt_katip_n = 0.0

    if len(averagewaitlist_aurora_w)>0:
        avgwt_aurora_w = sum(averagewaitlist_aurora_w.values()) / float(len(averagewaitlist_aurora_w))
    else:
        avgwt_aurora_w = 0.0

    if len(averagewaitlist_aurora_e)>0:
        avgwt_aurora_e = sum(averagewaitlist_aurora_e.values()) / float(len(averagewaitlist_aurora_e))
    else:
        avgwt_aurora_e = 0.0

    print(f"Average waiting time in Katipunan South: {avgwt_katip_s} s")
    print(f"Average waiting time in Katipunan North: {avgwt_katip_n} s")
    print(f"Average waiting time in Aurora West: {avgwt_aurora_w} s")
    print(f"Average waiting time in Aurora East: {avgwt_aurora_e} s")

    return avgwt_katip_s, avgwt_katip_n, avgwt_aurora_w, avgwt_aurora_e

def get_spawned_vehs():

    for veh_id in traci.simulation.getDepartedIDList():
        lane_id = traci.vehicle.getLaneID(veh_id)
        if lane_id in katip_south_edges:
            spawned_katip_s.append(1)
        elif lane_id in katip_north_edges:
            spawned_katip_n.append(1)
        elif lane_id in aurora_west_edges:
            spawned_aurora_w.append(1)
        else:
            spawned_aurora_e.append(1)

    total_spawned_katip_s = sum(spawned_katip_s)
    total_spawned_katip_n = sum(spawned_katip_n)
    total_spawned_aurora_w = sum(spawned_aurora_w)
    total_spawned_aurora_e = sum(spawned_aurora_e)
    '''
    print(f"Total vehicles spawned in Katipunan South: {total_spawned_katip_s}")
    print(f"Total vehicles spawned in Katipunan North: {total_spawned_katip_n}")
    print(f"Total vehicles spawned in Aurora West: {total_spawned_aurora_w}")
    print(f"Total vehicles spawned in Aurora East: {total_spawned_aurora_e}")
    '''
    return total_spawned_katip_s, total_spawned_katip_n, total_spawned_aurora_w, total_spawned_aurora_e
