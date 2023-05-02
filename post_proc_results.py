# Author: Jan Lendl R. Uy
# CoE 199 Post Processing of Traffic Data for Visualization

import os.path
import matplotlib.pyplot as plt
import numpy as np
import itertools
from bs4 import BeautifulSoup

# Store filenames of all relevant traffic data in two separate lists (fixed-time and mpc)
fixed_time_filenames = ["green_times.txt", "cycle.txt", "veh_count.txt", "q_length.txt", "q_time.txt", "flow.txt"]
mpc_filenames = ["mpc_green_times.txt", "mpc_cycle.txt", "mpc_veh_count.txt", "mpc_q_length.txt", 
                 "mpc_q_time.txt", "mpc_flow.txt"]

def read_fixed_time_data(filename, directory):

    # Store simulation results of fixed-time traffic signal control
    fixed_time_data = {"green_times" : [], "cycle" : [], "veh_count" : [], 
                   "q_length": [], "q_time" : [], "flow" : []}

    # Store results of fixed-time traffic signal control in arrays fixed_time_data 
    for file in filename:
        f = open(os.path.join(directory, file), "r")
        for line in f:
            # Removes ".txt" from iterable variable "file"
            # Obtains the appropriate list and appends data to that list
            list_data = fixed_time_data[file[:-4]]
            proc_line = line.split(" ")
            proc_line[-1] = proc_line[-1][:-1]
            proc_line.pop(0)
            proc_line = [float(i) for i in proc_line]
            list_data.append(proc_line)
        f.close()

    print("Finished storing the results of fixed-time simulation")
    return fixed_time_data

def read_mpc_data(filename, directory):

    # Store simulation results of MPC-based traffic signal control
    mpc_data = {"green_times" : [], "cycle" : [], "veh_count" : [], 
                 "q_length": [], "q_time" : [], "flow" : []}

    # Store results of MPC-based traffic signal control in arrays mpc_data
    for file in filename:
        f = open(os.path.join(directory, file), "r")
        for line in f:
            # Removes "mpc_" ".txt" from iterable variable "file"
            # Obtains the appropriate list and appends data to that list
            list_data = mpc_data[file[4:-4]]
            proc_line = line.split(" ")
            proc_line[-1] = proc_line[-1][:-1]
            proc_line.pop(0)
            proc_line = [float(i) for i in proc_line]
            list_data.append(proc_line)
        f.close()

    print("Finished storing the results of MPC-based simulation")
    return mpc_data

def plot_line_1_param(x, y, xlabel, ylabel, title):

    plt.figure()
    plt.plot(x, y, "g")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()

def plot_line_2_params(x, y1, y2, xlabel, ylabel, y1_label, y2_label, title):

    plt.figure()
    plt.plot(x, y1, "g-", label=y1_label)
    plt.plot(x, y2, "r-", label=y2_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()

def plot_line_3_params(x, y1, y2, y3, xlabel, ylabel, y1_label, y2_label, y3_label, title):

    plt.figure()
    plt.plot(x, y1, "g", label=y1_label)
    plt.plot(x, y2, "r", label=y2_label)
    plt.plot(x, y3, "m", label=y3_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()

def plot_line_4_params(x, y1, y2, y3, y4, xlabel, ylabel, y1_label, y2_label, y3_label, y4_label, title):

    plt.figure()
    plt.plot(x, y1, "g", label=y1_label)
    plt.plot(x, y2, "r", label=y2_label)
    plt.plot(x, y3, "m", label=y3_label)
    plt.plot(x, y4, "c", label=y4_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()


def plot_line_5_params(x, y1, y2, y3, y4, y5, xlabel, ylabel, y1_label, y2_label, y3_label, y4_label, y5_label, title):

    plt.figure()
    plt.plot(x, y1, "g", label=y1_label)
    plt.plot(x, y2, "r", label=y2_label)
    plt.plot(x, y3, "m", label=y3_label)
    plt.plot(x, y4, "c", label=y4_label)
    plt.plot(x, y5, "k", label=y5_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()

def plot_bar_2_params(x, y1, y2, xlabel, ylabel, y1_label, y2_label, title):

    plt.figure()
    plt.bar(x, y1, color="g", label=y1_label)
    plt.bar(x, y2, color="r", label=y2_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()

# Post process average queue length into per hour data
def post_proc_ql_cumul(hrs, data):

    end = 0
    ql_post_proc = [0.0]
    for i in range(hrs):
        if i > 0:
            end = 3600*(i+1)-2
        else:
            end = 3600*(i+1)-1
        temp_array = data["q_length"][end]
        #temp_array_conc = sum(temp_array, [])
        #temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        ql_post_proc.append(sum(temp_array)/float(len(temp_array)))

    print(f"Average queue length is: {ql_post_proc[-1]} m")
    return ql_post_proc

# Post process average queue time into per hour data

def post_proc_qt_cumul(hrs, data):

    end = 0
    qt_post_proc = [0.0]
    for i in range(hrs):
        if i > 0:
            end = 3600*(i+1)-2
        else:
            end = 3600*(i+1)-1           
        temp_array = data["q_time"][end]
        #temp_array_conc = sum(temp_array, [])
        #temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        qt_post_proc.append(sum(temp_array)/float(len(temp_array)))

    print(f"Average queue time is: {qt_post_proc[-1]} s")
    return qt_post_proc

# Post process flow rate into per hour data
def post_proc_flow_cumul(hrs, data):

    end = 0
    flow_post_proc = [0.0]
    for i in range(hrs):
        if i > 0:
            end = 3600*(i+1)-2
        else:
            end = 3600*(i+1)-1
        temp_array = data["flow"][end]
        #temp_array_conc = sum(temp_array, [])
        #temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        flow_post_proc.append(sum(temp_array)/float(len(temp_array)))

    print(f"Average flow rate is: {flow_post_proc[-1]} veh/hr")
    return flow_post_proc

# Post process average queue length into per hour data
def post_proc_ql(hrs, data):

    end = 0
    ql_post_proc = [0.0]
    for i in range(hrs):
        temp_array = data["q_length"][end]
        ql_post_proc.append(sum(temp_array)/float(len(temp_array)))

    print(f"Average queue length is: {ql_post_proc[-1]} m")
    return ql_post_proc

# Post process cycle time
def post_proc_cycle(data):
    c_proc = list(itertools.chain.from_iterable(data["cycle"]))
    return c_proc

# Post process green times
def post_proc_u(data):

    u_katip_s = []
    u_katip_n = []
    u_aurora_w = []
    u_aurora_e_katip_s = []
    u_aurora_e_aurora_w = []
  
    for i in range(len(data["green_times"])):
        katip_s = data["green_times"][i][0]
        katip_n = katip_s
        aurora_w = data["green_times"][i][2]
        aurora_e_katip_s = data["green_times"][i][3]
        aurora_e_aurora_w = data["green_times"][i][4]

        u_katip_s.append(katip_s)
        u_katip_n.append(katip_n)
        u_aurora_w.append(aurora_w)
        u_aurora_e_katip_s.append(aurora_e_katip_s)
        u_aurora_e_aurora_w.append(aurora_e_aurora_w)

    return u_katip_s, u_katip_n, u_aurora_w, u_aurora_e_katip_s, u_aurora_e_aurora_w

# Post process average queue length into per hour data
def post_proc_demand(step_size, hrs, directory):

    # Reading data from the xml file
    with open(directory, "r") as f:
        data = f.read()

    soup = BeautifulSoup(data, "xml")
    print("Successfully parsed the summary file of inserted vehicles")

    f.close()

    hourly_demand = [0.0]

    steps = soup.find_all("step")

    steps_per_s = int(1/step_size)
    #total_steps = (hrs+1)*3600*steps_per_s

    j = 1

    for i in range(len(steps)):

        time = float(steps[i]['time'])
        if time%3600.0 != 0 or time == 0:
            continue

        inserted_vehs = float(steps[i]["inserted"])
        if len(hourly_demand) > 1:
            hourly_demand.append(inserted_vehs-sum(hourly_demand[:j]))
        else:
            hourly_demand.append(inserted_vehs)
        j += 1

    return hourly_demand

def percent_improvement(post_proc_param1, post_proc_param2, param_name1, param_name2, quantity):

    if quantity not in ["q_length_cumul", "q_time_cumul" , "flow_cumul"]:
        return

    param1 = post_proc_param1[-1]
    param2 = post_proc_param2[-1]

    improvement = 0
    placeholder = ""

    if quantity in ["q_length_cumul", "q_time_cumul"]:

        if quantity == "q_length_cumul":
            placeholder = "Queue length"
        elif quantity == "q_time_cumul":
            placeholder = "Queue time"

        if param1 > param2:
            improvement = 1-(param2/param1)
            print(f"{placeholder} in {param_name2} is shorter than {param_name1} by {improvement*100}%")
        else:
            improvement = 1-(param1/param2)
            print(f"{placeholder} in {param_name1} is shorter than {param_name2} by {improvement*100}%")
    else:

        placeholder = "Flow rate"

        if param1 > param2:
            improvement = (param1/param2)-1
            print(f"{placeholder} in {param_name1} is faster than {param_name2} by {improvement*100}%")
        else:
            improvement = (param2/param1)-1
            print(f"{placeholder} in {param_name2} is faster than {param_name1} by {improvement*100}%")

def main():

    fixed_time_dir = "results\\fixed_time"
    mpc_dir_1 = "results\\cumulative_average\\test108\\"
    mpc_dir_2 = "results\\test11\\"
    #mpc_dir_3 = "results\\test12(extended_roads,umin=15,n=5)\\"

    num_hours = 14

    # Simulation time stored as an array
    sim_hr = ["6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", 
            "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
    sim_sec = np.arange(1,50401,1)

    # Actual hourly traffic demand from MMDA data
    demand_actual = [0, 8491, 9618, 10305, 7898, 7271, 6654, 6585, 
                            8381, 8106, 8871, 9462, 10776, 9620, 8499]

    # Obtain values of traffic data from simulations
    fixed_time_data = read_fixed_time_data(fixed_time_filenames, fixed_time_dir)
    mpc_data_1 = read_mpc_data(mpc_filenames, mpc_dir_1)
    mpc_data_2 = read_mpc_data(mpc_filenames, mpc_dir_2)
    #mpc_data_3 = read_mpc_data(mpc_filenames, mpc_dir_3)

    ql_fixed_time = post_proc_ql_cumul(num_hours, fixed_time_data)
    ql_mpc_1 = post_proc_ql_cumul(num_hours, mpc_data_1)
    ql_mpc_2 = post_proc_ql_cumul(num_hours, mpc_data_2)
    #ql_mpc_3 = post_proc_ql(num_hours, mpc_data_3)

    qt_fixed_time = post_proc_qt_cumul(num_hours, fixed_time_data)
    qt_mpc_1 = post_proc_qt_cumul(num_hours, mpc_data_1)
    qt_mpc_2 = post_proc_qt_cumul(num_hours, mpc_data_2)
    #qt_mpc_3 = post_proc_qt(num_hours, mpc_data_3)

    flow_fixed_time = post_proc_flow_cumul(num_hours, fixed_time_data)
    flow_mpc_1 = post_proc_flow_cumul(num_hours, mpc_data_1)
    flow_mpc_2 = post_proc_flow_cumul(num_hours, mpc_data_2)
    #flow_mpc_3 = post_proc_flow(num_hours, mpc_data_3)

    c_fixed_time = post_proc_cycle(fixed_time_data)
    c_mpc_1 = post_proc_cycle(mpc_data_1)
    c_mpc_2 = post_proc_cycle(mpc_data_2)

    #demand_fixed_time = post_proc_demand(0.5, 14, "results\\summary_003_fixed_time.xml")
    #demand_mpc = post_proc_demand(0.5, 14, "results\\summary_003_mpc.xml")

    gtf_katip_s, gtf_katip_n, gtf_aurora_w, gtf_aurora_e_katip_s, gtf_aurora_e_aurora_w = post_proc_u(fixed_time_data)
    gt1_katip_s, gt1_katip_n, gt1_aurora_w, gt1_aurora_e_katip_s, gt1_aurora_e_aurora_w = post_proc_u(mpc_data_1)
    gt2_katip_s, gt2_katip_n, gt2_aurora_w, gt2_aurora_e_katip_s, gt2_aurora_e_aurora_w = post_proc_u(mpc_data_2)
    '''
    plot_line_2_params(sim_hr, ql_fixed_time, ql_mpc_2, "Time of Day (hr:min)", "Average Queue Length (m)", 
              "Fixed-time TSC", "MPC-based TSC", "Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_2_params(sim_hr, qt_fixed_time, qt_mpc_2, "Time of Day (hr:min)", "Average Queue Time (s)", 
              "Fixed-time TSC", "MPC-based TSC", "Average Queue Time in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_2_params(sim_hr, flow_fixed_time, flow_mpc_2, "Time of Day (hr:min)", "Flow Rate (veh/hr)", 
              "Fixed-time TSC", "MPC-based TSC", "Flow Rate of Traffic in the Katipunan Ave. - Aurora Blvd. Intersection")
    
    '''
    plot_line_3_params(sim_hr, ql_fixed_time, ql_mpc_1, ql_mpc_2, "Time of Day (hr:min)", "Average Queue Length (m)", 
              "Fixed-time TSC", "MPC-based TSC Current Best", "MPC-based TSC Test", "Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_3_params(sim_hr, qt_fixed_time, qt_mpc_1, qt_mpc_2, "Time of Day (hr:min)", "Average Queue Time (s)", 
              "Fixed-time TSC", "MPC-based TSC Current Best", "MPC-based TSC Test", "Average Queue Time in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_3_params(sim_hr, flow_fixed_time, flow_mpc_1, flow_mpc_2, "Time of Day (hr:min)", "Flow Rate (veh/hr)", 
              "Fixed-time TSC", "MPC-based TSC Current Best", "MPC-based TSC Test", "Flow Rate of Traffic in the Katipunan Ave. - Aurora Blvd. Intersection")
    
    '''
    plot_line_2_params(sim_hr, demand_fixed_time, demand_actual, "Time of Day (hr:min)", "Number of Vehicles", "Simulator-generated demand", "Actual demand", 
                       "Hourly Traffic in the Intersection for Fixed-time TSC Simulation")
    plot_line_2_params(sim_hr, demand_mpc, demand_actual, "Time of Day (hr:min)", "Number of Vehicles", "Simulator-generated demand", "Actual demand", 
                       "Hourly Traffic in the Intersection for MPC-based TSC Simulation")
    '''

    plot_line_1_param(sim_sec, c_mpc_2, "Time (s)", "Cycle Time (s)", "Cycle Time of the MPC-based Traffic Signal Control")
    plot_line_5_params(sim_sec, gt2_katip_s, gt2_katip_n, gt2_aurora_w, gt2_aurora_e_katip_s, gt2_aurora_e_aurora_w, "Time (s)", 
                       "Green Times (s)", "Green Time of Katipunan South ", "Green Time of Katipunan North", "Green Time of Aurora West", 
                       "Green Time of Aurora East to Katipunan South", "Green Time of Aurora East to West", "Green Times of the Stoplights in MPC-based TSC")
    
    
    percent_improvement(ql_mpc_1, ql_mpc_2, "MPC-based TSC Current Best", "MPC-based TSC Test", "q_length")
    percent_improvement(qt_mpc_1, qt_mpc_2, "MPC-based TSC Current Best", "MPC-based TSC Test", "q_time")
    percent_improvement(flow_mpc_1, flow_mpc_2, "MPC-based TSC Current Best", "MPC-based TSC Test", "flow")

    '''
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(sim_hr, ql_fixed_time, "g")
    ax1.plot(sim_hr, ql_mpc_2, "r")
    ax2.bar(sim_hr, demand_mpc, "m")

    ax1.set_xlabel("Time of Day (hr:min)")
    ax1.set_ylabel("Average Queue Length (m)")
    ax2.set_ylabel("Number of vehicles (veh)")

    plt.title("Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection")
    plt.legend()
    plt.gcf().autofmt_xdate()
    
    plt.figure()
    plt.plot(sim_sec, gtf_katip_s, "g", label="Green Time of Katipunan South and North (Fixed-time)")
    plt.plot(sim_sec, gtf_aurora_w, "m", label="Green Time of Aurora West (Fixed-time)")
    plt.plot(sim_sec, gtf_aurora_e_katip_s, "c", label="Green Time of Aurora East to Katipunan South (Fixed-time)")
    plt.plot(sim_sec, gtf_aurora_e_aurora_w, "k", label="Green Time of Aurora East to West (Fixed-time)")

    plt.plot(sim_sec, gt_katip_s, "g--", label="Green Time of Katipunan South and North (MPC-based)")
    plt.plot(sim_sec, gt_aurora_w, "m--", label="Green Time of Aurora West (MPC-based)")
    plt.plot(sim_sec, gt_aurora_e_katip_s, "c--", label="Green Time of Aurora East to Katipunan South (MPC-based)")
    plt.plot(sim_sec, gt_aurora_e_aurora_w, "k--", label="Green Time of Aurora East to West (MPC-based)")

    plt.title("Green Times of the Stoplights in the Intersection")
    plt.xlabel("Time (s)")
    plt.ylabel("Green Times (s)")
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()
    '''
    plt.show()

if __name__ == "__main__":
    main()