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
    plt.xticks([3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800, 50400])
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
    plt.xticks([3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800, 50400])
    plt.gcf().autofmt_xdate()

def plot_line_4_params(x, y1, y2, y3, y4, xlabel, ylabel, y1_label, y2_label, y3_label, y4_label, title):

    plt.figure(figsize=(8,8))
    plt.plot(x, y1, "b", label=y1_label)
    plt.plot(x, y2, "tab:orange", label=y2_label)
    plt.plot(x, y3, "g", label=y3_label)
    plt.plot(x, y4, "m", label=y4_label)
    plt.title(title, fontsize=15)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    #plt.xlim(0)
    plt.ylim((0,65))
    #plt.xticks(x[0::3600], rotation=45)
    plt.xticks(x[0::600], rotation=45)
    plt.legend(loc = "upper left", prop={"size": 11})
    #plt.gcf().autofmt_xdate()


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
    plt.xticks([3600, 7200, 10800, 14400, 18000, 21600, 25200, 28800, 32400, 36000, 39600, 43200, 46800, 50400])
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
def post_proc_ql(data):

    ql_post_proc = [0.0]
    for i in range(int(50400/900)):
        temp_array = data["q_length"][i]
        #temp_array_conc = sum(temp_array, [])
        #temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        ql_post_proc.append(temp_array[0])

    return ql_post_proc

# Post process average queue time into per hour data

def post_proc_qt(data):

    qt_post_proc = [0.0]
    for i in range(int(50400/900)):        
        temp_array = data["q_time"][i]
        #temp_array_conc = sum(temp_array, [])
        #temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        qt_post_proc.append(temp_array[0])

    return qt_post_proc

# Post process flow rate into per hour data
def post_proc_flow(data):

    #print(f"data = {data}")
    flow_post_proc = [0.0]
    for i in range(int(50400/900)):
        temp_array = data["flow"][i]
        #temp_array_conc = sum(temp_array, [])
        #temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        flow_post_proc.append(temp_array[0])

    return flow_post_proc

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

    fixed_time_dir = "fixed_time"
    mpc_dir_1 = "test414\\"
    mpc_dir_2 = "test289\\"
    #mpc_dir_3 = "results\\test12(extended_roads,umin=15,n=5)\\"

    num_hours = 14

    # Simulation time stored as an array
    start_hr = 6
    start_min = 0
    start_sec = 0
    sim_hr = []
    temp_min = ""
    temp_sec = ""
    for n in range(50400):

        if n > 0:
            if n%3600 == 0:
                start_hr += 1
            if n%60 == 0:
                if n%3600 == 0:
                    start_min = 0
                else:
                    start_min += 1
                start_sec = 0
            
        if start_sec < 10:
            temp_sec = "0"+str(start_sec)
        else:
            temp_sec = str(start_sec)

        if start_min < 10:
            temp_min = "0"+str(start_min)
        else:
            temp_min = str(start_min)

        sim_hr.append(f"{start_hr}:{temp_min}:{temp_sec}")

        start_sec += 1

    sim_sec = np.arange(1,50401,1)
    sim_window = np.arange(0,51300,900)

    # Actual hourly traffic demand from MMDA data
    demand_actual = [0, 8491, 9618, 10305, 7898, 7271, 6654, 6585, 
                            8381, 8106, 8871, 9462, 10776, 9620, 8499]

    # Obtain values of traffic data from simulations
    fixed_time_data = read_fixed_time_data(fixed_time_filenames, fixed_time_dir)
    mpc_data_1 = read_mpc_data(mpc_filenames, mpc_dir_1)
    mpc_data_2 = read_mpc_data(mpc_filenames, mpc_dir_2)

    gt1_katip_s, gt1_katip_n, gt1_aurora_w, gt1_aurora_e_katip_s, gt1_aurora_e_aurora_w = post_proc_u(mpc_data_1)
    gt2_katip_s, gt2_katip_n, gt2_aurora_w, gt2_aurora_e_katip_s, gt2_aurora_e_aurora_w = post_proc_u(mpc_data_2)
    '''
    plot_line_4_params(sim_hr, gt1_katip_s, gt1_aurora_w, gt1_aurora_e_katip_s, gt1_aurora_e_aurora_w, "Time (s)", 
                       "Green Time (s)", "Green Time of Katipunan South/North", "Green Time of Aurora West", 
                       "Green Time of Aurora East to Katipunan South", "Green Time of Aurora East to West", "Green Times of the Stoplights in the Intersection")
    
    plot_line_4_params(sim_hr, gt2_katip_s, gt2_aurora_w, gt2_aurora_e_katip_s, gt2_aurora_e_aurora_w, "Time (s)", 
                       "Green Time (s)", "Green Time of Katipunan South/North", "Green Time of Aurora West", 
                       "Green Time of Aurora East to Katipunan South", "Green Time of Aurora East to West", "Green Times of the Stoplights in Baseline")
    '''
    
    time = 14400
    plot_line_4_params(sim_hr[time:time+3500], gt1_katip_s[time:time+3500], gt1_aurora_w[time:time+3500], gt1_aurora_e_katip_s[time:time+3500], gt1_aurora_e_aurora_w[time:time+3500], "Time (s)", 
                       "Green Time (s)", "Green Time of Katipunan South/North", "Green Time of Aurora West", 
                       "Green Time of Aurora East to Katipunan South", "Green Time of Aurora East to West", "Green Times of the Stoplights from 10:00 AM to 11:00 AM")
    '''
    plot_line_5_params(sim_sec, gt2_katip_s, gt2_katip_n, gt2_aurora_w, gt2_aurora_e_katip_s, gt2_aurora_e_aurora_w, "Time (s)", 
                       "Green Times (s)", "Green Time of Katipunan South", "Green Time of Katipunan North", "Green Time of Aurora West", 
                       "Green Time of Aurora East to Katipunan South", "Green Time of Aurora East to West", "Green Times of the Stoplights in MPC-based TSC")
    '''

    ql_fixed_time = post_proc_ql(fixed_time_data)
    ql_mpc_1 = post_proc_ql(mpc_data_1)
    ql_mpc_2 = post_proc_ql(mpc_data_2)

    qt_fixed_time = post_proc_qt(fixed_time_data)
    qt_mpc_1 = post_proc_qt(mpc_data_1)
    qt_mpc_2 = post_proc_qt(mpc_data_2)

    flow_fixed_time = post_proc_flow(fixed_time_data)
    flow_mpc_1 = post_proc_flow(mpc_data_1)
    flow_mpc_2 = post_proc_flow(mpc_data_2)

    plot_line_2_params(sim_window, ql_mpc_1, ql_mpc_2, "Time of Day (hr:min)", "Average Queue Length (m)", 
            "Test", "Baseline", "Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_2_params(sim_window, qt_mpc_1, qt_mpc_2, "Time of Day (hr:min)", "Average Queue Time (s)", 
            "Test", "Baseline", "Average Queue Time in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_2_params(sim_window, flow_mpc_1, flow_mpc_2, "Time of Day (hr:min)", "Flow Rate (veh/hr)", 
            "Test", "Baseline", "Flow Rate of Traffic in the Katipunan Ave. - Aurora Blvd. Intersection")
    
    plt.show()

if __name__ == "__main__":
    main()