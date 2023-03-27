import os.path
import matplotlib.pyplot as plt
import numpy as np
import itertools

# Store filenames of all relevant traffic data in two separate lists (fixed-time and mpc)
fixed_time_filenames = ["green_times.txt", "cycle.txt", "veh_count.txt", "q_length.txt", "q_time.txt", "flow.txt", "spawned.txt"]
mpc_filenames = ["mpc_green_times.txt", "mpc_cycle.txt", "mpc_veh_count.txt", "mpc_q_length.txt", "mpc_q_time.txt", "mpc_flow.txt", "mpc_spawned.txt"]

def read_fixed_time_data(filename, directory):

    # Store simulation results of fixed-time traffic signal control
    fixed_time_data = {"green_times" : [], "cycle" : [], "veh_count" : [], 
                   "q_length": [], "q_time" : [], "flow" : [], "spawned" : []}

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
                 "q_length": [], "q_time" : [], "flow" : [], "spawned" : []}

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
    plt.legend()
    plt.gcf().autofmt_xdate()

def plot_line_2_params(x, y1, y2, xlabel, ylabel, y1_label, y2_label, title):

    plt.figure()
    plt.plot(x, y1, "g", label=y1_label)
    plt.plot(x, y2, "r", label=y2_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
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
    plt.legend()
    plt.gcf().autofmt_xdate()

def plot_bar_2_params(x, y1, y2, xlabel, ylabel, y1_label, y2_label, title):

    plt.figure()
    plt.bar(x, y1, color="g", label=y1_label)
    plt.bar(x, y2, color="r", label=y2_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.gcf().autofmt_xdate()

# Post process average queue length into per hour data
def post_proc_ql(hrs, data):

    ql_post_proc = []
    for i in range(hrs):
        if i > 0:
            start = (i*3600)-1
            end = 3600*(i+1)-1
            temp_array = data["q_length"][start:end]
        else:
            temp_array = data["q_length"][0:3599]
        #temp_array_conc = sum(temp_array, [])
        temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        ql_post_proc.append(sum(temp_array_conc)/float(len(temp_array_conc)))
    print(f"ql_post_proc = {ql_post_proc[-1]}")
    return ql_post_proc

# Post process average queue time into per hour data

def post_proc_qt(hrs, data):

    qt_post_proc = []
    for i in range(hrs):
        if i > 0:
            start = (i*3600)-1
            end = 3600*(i+1)-1
            temp_array = data["q_time"][start:end]
        else:
            temp_array = data["q_time"][0:3599]
        #temp_array_conc = sum(temp_array, [])
        temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        qt_post_proc.append(sum(temp_array_conc)/float(len(temp_array_conc)))
    print(f"qt_post_proc = {qt_post_proc[-1]}")
    return qt_post_proc

# Post process flow rate into per hour data
def post_proc_flow(hrs, data):

    flow_post_proc = []
    for i in range(hrs):
        if i > 0:
            start = (i*3600)-1
            end = 3600*(i+1)-1
            temp_array = data["flow"][start:end]
        else:
            temp_array = data["flow"][0:3599]
        #temp_array_conc = sum(temp_array, [])
        temp_array_conc = list(itertools.chain.from_iterable(temp_array))
        flow_post_proc.append(sum(temp_array_conc)/float(len(temp_array_conc)))

    u_katip_s = []
    u_katip_n = []
    u_aurora_w = []
    u_aurora_e = []

    '''
    for i in range(len(data["flow"])):
        katip_s = data["flow"][i][0]
        katip_n = data["flow"][i][1]
        aurora_w = data["flow"][i][2]
        aurora_e = data["flow"][i][3]

        u_katip_s.append(katip_s)
        u_katip_n.append(katip_n)
        u_aurora_w.append(aurora_w)
        u_aurora_e.append(aurora_e)
    
    print(f"max flow of katip_s = {max(u_katip_s)}")
    print(f"max flow of katip_n = {max(u_katip_n)}")
    print(f"max flow of aurora_w = {max(u_aurora_w)}")
    print(f"max flow of aurora_e = {max(u_aurora_e)}")
    '''
    print(f"flow_post_proc = {flow_post_proc[-1]}")
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
def post_proc_spawned(data):

    spawned_katip_s = []
    spawned_katip_n = []
    spawned_aurora_w = []
    spawned_aurora_e = []
    total_spawned_int = []

    for i in range(len(data["spawned"])):
        katip_s = data["spawned"][i][0]
        katip_n = data["spawned"][i][1]
        aurora_w = data["spawned"][i][2]
        aurora_e = data["spawned"][i][3]

        spawned_katip_s.append(katip_s)
        spawned_katip_n.append(katip_n)
        spawned_aurora_w.append(aurora_w)
        spawned_aurora_e.append(aurora_e)
        total_spawned_int.append(katip_s+katip_n+aurora_w+aurora_e)

    total_spawned = int(spawned_katip_s[-1]+spawned_katip_n[-1]+spawned_aurora_w[-1]+spawned_aurora_e[-1])

    #print(f"Total number of vehicles spawned in the simulation = {total_spawned}")

    return spawned_katip_s, spawned_katip_n, spawned_aurora_w, spawned_aurora_e, total_spawned_int

def percent_improvement(param1, param2, param_name1, param_name2, quantity):

    if quantity not in ["q_length", "q_time" , "flow"]:
        return

    param1_vals = list(itertools.chain.from_iterable(param1[quantity]))
    param2_vals = list(itertools.chain.from_iterable(param2[quantity]))

    area_param1 = np.trapz(param1_vals)
    area_param2 = np.trapz(param2_vals)

    improvement = 0
    placeholder = ""

    if quantity in ["q_length", "q_time"]:

        if quantity == "q_length":
            placeholder = "Queue length"
        elif quantity == "q_time":
            placeholder = "Queue time"

        if area_param1 > area_param2:
            improvement = 1-(area_param2/area_param1)
            print(f"{placeholder} in {param_name2} is shorter than {param_name1} by {improvement*100}%")
        else:
            improvement = 1-(area_param1/area_param2)
            print(f"{placeholder} in {param_name1} is shorter than {param_name2} by {improvement*100}%")
    else:

        placeholder = "Flow rate"

        if area_param1 > area_param2:
            improvement = (area_param1/area_param2)-1
            print(f"{placeholder} in {param_name1} is faster than {param_name2} by {improvement*100}%")
        else:
            improvement = (area_param2/area_param1)-1
            print(f"{placeholder} in {param_name2} is faster than {param_name1} by {improvement*100}%")

'''
# Obtain maximum number of vehicles to compute saturation flow rate of each road

veh_counts_katip_s = []
veh_counts_katip_n = []
veh_counts_aurora_w = []
veh_counts_aurora_e = []

for i in range(num_hours):

    if i > 0:
        start = (i*3600)-1
        end = 3600*(i+1)-1
        temp_array = fixed_time_data["veh_count"][start:end]
    else:
        temp_array = fixed_time_data["veh_count"][0:3599]

    print(f"{temp_array}\n")
    
    veh_count_katip_s = mpc_data["veh_count"][i][0]
    veh_count_katip_n = mpc_data["veh_count"][i][1]
    veh_count_aurora_w = mpc_data["veh_count"][i][2]
    veh_count_aurora_e = mpc_data["veh_count"][i][3]

    #temp_array_conc = sum(temp_array, [])
    temp_array_conc = list(itertools.chain.from_iterable(temp_array))
    flow_fixed_post_proc.append(sum(temp_array_conc)/float(len(temp_array_conc)))

    veh_counts_katip_s.append(veh_count_katip_s)
    veh_counts_katip_n.append(veh_count_katip_n)
    veh_counts_aurora_w.append(veh_count_aurora_w)
    veh_counts_aurora_e.append(veh_count_aurora_e)


max_cap_katip_s = max(veh_counts_katip_s)
max_cap_katip_n = max(veh_counts_katip_n)
max_cap_aurora_w = max(veh_counts_aurora_w)
max_cap_aurora_e = max(veh_counts_aurora_e)
'''

def main():

    fixed_time_dir = "results\\fixed_time"
    mpc_dir_1 = "results\\test1(cmin=60,cmax=100,umin=15,n=5)\\"
    #mpc_dir_2 = "results\\test30\\"
    #mpc_dir_3 = "results\\test12(extended_roads,umin=15,n=5)\\"

    num_hours = 14

    # Simulation time stored as an array
    sim_hr = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", 
            "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
    sim_sec = np.arange(1,50400,1)

    # Obtain values of traffic data from simulations
    fixed_time_data = read_fixed_time_data(fixed_time_filenames, fixed_time_dir)
    mpc_data_1 = read_mpc_data(mpc_filenames, mpc_dir_1)
    #mpc_data_2 = read_mpc_data(mpc_filenames, mpc_dir_2)
    #mpc_data_3 = read_mpc_data(mpc_filenames, mpc_dir_3)


    ql_fixed_time = post_proc_ql(num_hours, fixed_time_data)
    ql_mpc_1 = post_proc_ql(num_hours, mpc_data_1)
    #ql_mpc_2 = post_proc_ql(num_hours, mpc_data_2)
    #ql_mpc_3 = post_proc_ql(num_hours, mpc_data_3)

    qt_fixed_time = post_proc_qt(num_hours, fixed_time_data)
    qt_mpc_1 = post_proc_qt(num_hours, mpc_data_1)
    #qt_mpc_2 = post_proc_qt(num_hours, mpc_data_2)
    #qt_mpc_3 = post_proc_qt(num_hours, mpc_data_3)

    flow_fixed_time = post_proc_flow(num_hours, fixed_time_data)
    flow_mpc_1 = post_proc_flow(num_hours, mpc_data_1)
    #flow_mpc_2 = post_proc_flow(num_hours, mpc_data_2)
    #flow_mpc_3 = post_proc_flow(num_hours, mpc_data_3)

    spawned_vehs = post_proc_spawned(fixed_time_data)

    c_times = post_proc_cycle(mpc_data_1)

    gt_katip_s, gt_katip_n, gt_aurora_w, gt_aurora_e_katip_s, gt_aurora_e_aurora_w = post_proc_u(mpc_data_1)

    
    plot_line_2_params(sim_hr, ql_fixed_time, ql_mpc_1, "Time of Day (hr:min)", "Average Queue Length (m)", 
              "Fixed-time TSC", "MPC-based TSC Test 1", "Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_2_params(sim_hr, qt_fixed_time, qt_mpc_1, "Time of Day (hr:min)", "Average Queue Time (s)", 
              "Fixed-time TSC", "MPC-based TSC Test 1", "Average Queue Time in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_2_params(sim_hr, flow_fixed_time, flow_mpc_1, "Time of Day (hr:min)", "Flow Rate (veh/hr)", 
              "Fixed-time TSC", "MPC-based TSC Test 1", "Flow Rate of Traffic in the Katipunan Ave. - Aurora Blvd. Intersection")

    '''
    plot_line_3_params(sim_hr, ql_fixed_time, ql_mpc_1, ql_mpc_2, "Time of Day (hr:min)", "Average Queue Length (m)", 
              "Fixed-time TSC", "MPC-based TSC Test 1", "MPC-based TSC Test 30", "Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_3_params(sim_hr, qt_fixed_time, qt_mpc_1, qt_mpc_2, "Time of Day (hr:min)", "Average Queue Time (s)", 
              "Fixed-time TSC", "MPC-based TSC Test 1", "MPC-based TSC Test 30", "Average Queue Time in the Katipunan Ave. - Aurora Blvd. Intersection")
    plot_line_3_params(sim_hr, flow_fixed_time, flow_mpc_1, flow_mpc_2, "Time of Day (hr:min)", "Flow Rate (veh/hr)", 
              "Fixed-time TSC", "MPC-based TSC Test 1", "MPC-based TSC Test 30", "Flow Rate of Traffic in the Katipunan Ave. - Aurora Blvd. Intersection")
    

    plot_line_4_params(sim_sec, spawned_vehs[0], spawned_vehs[1], spawned_vehs[2], spawned_vehs[3], "Time (s)", "Vehicle count", "Katipunan South", "Katipunan North", "Aurora West", "Aurora East",
                       "Number of vehicles spawned from 6:00 AM to 8:00 PM")
    plot_line_1_param(sim_sec, spawned_vehs[4], "Time (s)", "Vehicle count", "Total number of vehicles spawned from 6:00 AM to 8:00 PM")
    '''

    plot_line_1_param(sim_sec, c_times, "Time (s)", "Cycle Time (s)", "Cycle Time of MPC-based Traffic Signal Control")
    plot_line_5_params(sim_sec, gt_katip_s, gt_katip_n, gt_aurora_w, gt_aurora_e_katip_s, gt_aurora_e_aurora_w, "Time (s)", 
                       "Green Times (s)", "Green Time of Katipunan South ", "Green Time of Katipunan Nprth", "Green Time of Aurora West", 
                       "Green Time of Aurora East to Katipunan South", "Green Time of Aurora East to West", "Change in Green Times of the Stoplights in the Intersection")
    
    percent_improvement(fixed_time_data, mpc_data_1, "Fixed-time TSC", "MPC-based TSC Test 1", "q_length")
    percent_improvement(fixed_time_data, mpc_data_1, "Fixed-time TSC", "MPC-based TSC Test 1", "q_time")
    percent_improvement(fixed_time_data, mpc_data_1, "Fixed-time TSC", "MPC-based TSC Test 1", "flow")
    
    plt.show()

if __name__ == "__main__":
    main()