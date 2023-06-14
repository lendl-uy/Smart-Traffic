import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

'''
# TRENDS IN MINIMUM GREEN TIME

avg_ql = np.array([6.83, 7.51, 3.85, 7.29, -0.88, 0.30, 0.31, 0.35, 2.79, -3.07, -2.53])

avg_qt = np.array([-5.19, 15.06, 16.23, 12.36, 10.58, 14.01, 2.08, 6.56, 14.59, 15.19, 14.77])

avg_flow = np.array([1.27, 1.24, 1.29, 1.19, 1.01, 1.02, 0.84, 0.87, 0.89, 1.17, 1.28])

u_min = np.array([10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40])

plt.figure()
plt.plot(u_min, avg_ql, "b")
plt.title("Average Queue Length Improvement vs. Minimum Green Time")
plt.xlabel("Minimum Green Time (s)")
plt.ylabel("Performance Improvement of Average Queue Length (%)")
plt.axhline(0, color='black', linewidth=.5)
plt.xlim(10)
plt.ylim(-5, 10)
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(u_min, avg_qt, "b")
plt.title("Average Queue Time Improvement vs. Minimum Green Time")
plt.xlabel("Minimum Green Time (s)")
plt.ylabel("Performance Improvement of Average Queue Time (%)")
plt.axhline(0, color='black', linewidth=.5)
plt.xlim(10)
plt.ylim(-7, 20)
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(u_min, avg_flow, "b")
plt.title("Average Flow Rate Improvement vs. Minimum Green Time")
plt.xlabel("Minimum Green Time (s)")
plt.ylabel("Performance Improvement of Average Flow Rate (%)")
plt.xlim(10)
plt.ylim(0, 4)
plt.legend()
plt.gcf().autofmt_xdate()

#plt.show()

# SYSTEM STATE TRAJECTORY

def plot_line_2_params(x, y1, y2, xlabel, ylabel, y1_label, y2_label, title):

    plt.figure()
    plt.stem(x, y1, "g-", label=y1_label)
    plt.stem(x, y2, "r-", label=y2_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0)
    plt.ylim(0)
    plt.legend()
    plt.gcf().autofmt_xdate()

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
    print(f"hourly_demand = {hourly_demand}")
    return hourly_demand

# Actual hourly traffic demand from MMDA data
demand_actual = [0, 8491, 9618, 10305, 7898, 7271, 6654, 6585, 8381, 8106, 8871, 9462, 10776, 9620, 8499]

sim_hr = ["6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]

demand_mpc = post_proc_demand(0.5, 14, "results\\summary_003_mpc.xml")

plot_line_2_params(sim_hr, demand_mpc, demand_actual, "Time of Day (hr:min)", "Number of Vehicles", "Simulator-generated demand", "Actual demand", "Hourly Traffic in the Intersection for MPC-based TSC Simulation")

plt.show()
'''

'''
C = 75
k = np.arange(0,C*12,1)

trajectory_katip_s = [14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13]
trajectory_katip_n = [34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89]
trajectory_aurora_w = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
trajectory_aurora_e_w = [50, 57, 64, 70, 77, 84, 91, 98, 104, 111, 118, 125]
trajectory_aurora_e_katip_s = [8,9,10,11,12,13,14,15,17,18,19,20,22]

actual_katip_s = [14, 12, 11, 12, 12, 15, 13, 11, 12, 14, 10, 10]
actual_katip_n = [34, 38, 46, 50, 5, 54, 59, 57, 61, 66, 52, 45]
actual_aurora_w = [15, 22, 21, 20, 21, 20, 20, 22, 23, 20, 18, 21]
actual_aurora_e_w = [50, 75, 78, 80, 80, 78, 80, 78, 77, 76, 86, 109]
actual_aurora_e_katip_s = [8, 12, 13, 14, 14, 12, 12, 12, 11, 10, 8, 15]

trajectory_katip_s_new = []
trajectory_katip_n_new = []
trajectory_aurora_w_new = []
trajectory_aurora_e_w_new = []
trajectory_aurora_e_katip_s_new = []

actual_katip_s_new = []
actual_katip_n_new = []
actual_aurora_w_new = []
actual_aurora_e_w_new = []
actual_aurora_e_katip_s_new = []
for i in range(12):

    trajectory_katip_s_new += [trajectory_katip_s[i]]*C
    trajectory_katip_n_new += [trajectory_katip_n[i]]*C
    trajectory_aurora_w_new += [trajectory_aurora_w[i]]*C
    trajectory_aurora_e_w_new += [trajectory_aurora_e_w[i]]*C
    trajectory_aurora_e_katip_s_new += [trajectory_aurora_e_katip_s[i]]*C

    actual_katip_s_new += [actual_katip_s[i]]*C
    actual_katip_n_new += [actual_katip_n[i]]*C
    actual_aurora_w_new += [actual_aurora_w[i]]*C
    actual_aurora_e_w_new += [actual_aurora_e_w[i]]*C
    actual_aurora_e_katip_s_new +=[actual_aurora_e_katip_s[i]]*C

plt.figure()
plt.plot(k, trajectory_katip_s_new, "g--", label="Predicted")
plt.plot(k, actual_katip_s_new, "g", label="Actual")
plt.title("Predicted Vehicle Count vs. Actual Vehicle Count in Katipuan Ave. South, N = 12, C = 75")
plt.ylim(0, max(trajectory_katip_s_new)+10)
plt.xlabel("Time (s)")
plt.ylabel("Number of vehicles (veh)")
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(k, trajectory_katip_n_new, "r--", label="Predicted")
plt.plot(k, actual_katip_n_new, "r", label="Actual")
plt.title("Predicted Vehicle Count vs. Actual Vehicle Count in Katipuan Ave. North, N = 12, C = 75")
plt.ylim(0, max(trajectory_katip_n_new)+10)
plt.xlabel("Time (s)")
plt.ylabel("Number of vehicles (veh)")
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(k, trajectory_aurora_w_new, "m--", label="Predicted")
plt.plot(k, actual_aurora_w_new, "m", label="Actual")
plt.title("Predicted Vehicle Count vs. Actual Vehicle Count in Aurora Blvd. West, N = 12, C = 75")
plt.ylim(0, max(trajectory_aurora_w_new)+10)
plt.xlabel("Time (s)")
plt.ylabel("Number of vehicles (veh)")
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(k, trajectory_aurora_e_w_new, "c--", label="Predicted")
plt.plot(k, actual_aurora_e_w_new, "c", label="Actual")
plt.title("Predicted Vehicle Count vs. Actual Vehicle Count in Aurora Blvd. East Lanes 1-3, N = 12, C = 75")
plt.ylim(0, max(trajectory_aurora_e_w_new)+10)
plt.xlabel("Time (s)")
plt.ylabel("Number of vehicles (veh)")
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(k, trajectory_aurora_e_katip_s_new, "k--", label="Predicted")
plt.plot(k, actual_aurora_e_katip_s_new, "k", label="Actual")
plt.title("Predicted Vehicle Count vs. Actual Vehicle Count in Aurora Blvd. Lane 4, N = 12, C = 75")
plt.ylim(0, max(trajectory_aurora_e_katip_s_new)+10)
plt.xlabel("Time (s)")
plt.ylabel("Number of vehicles (veh)")
plt.legend()
plt.gcf().autofmt_xdate()

#plt.xlim(10)
#plt.ylim(-7, 20)

plt.show()
'''

# Plot Fixed-time TSC vs MPC-based TSC for lower cycle times
fixed_time_perf_ql = [11.67973289,13.55946825,15.9475019,18.53459987,28.7639795]
mpc_based_perf_ql = [11.42316725,13.20130018,14.85116212,16.98508226,27.02271858]
fixed_time_perf_qt = [22.37023087,22.91194918,25.17958151,27.77935478,33.74459006]
mpc_based_perf_qt = [19.78153969,20.30318602,21.8700803,23.81856295,30.09917043]
fixed_time_perf_flow = [8467.785714,8495.5,8523.785714,8535.357143,8595.2857143]
mpc_based_perf_flow = [8575.928571,8618,8646,8663.571429,8687.7857143]

cycle_times = [70, 80, 90, 100, 154]
width = 4.5

# Plot Fixed-time TSC vs MPC-based TSC for different demand profiles
fixed_time_profile_1 = [26.57614985,13.14624454,7727.714286]
mpc_based_profile_1 = [26.57614985,13.14624454,7727.714286]
fixed_time_profile_2 = [26.57614985,13.14624454,7727.714286]
mpc_based_profile_2 = [26.57614985,13.14624454,7727.714286]
fixed_time_profile_3 = [26.57614985,13.14624454,7727.714286]
mpc_based_profile_3 = [26.57614985,13.14624454,7727.714286]
fixed_time_profile_4 = [26.57614985,13.14624454,7727.714286]
mpc_based_profile_4 = [26.57614985,13.14624454,7727.714286]

# Plot MPC-based TSC for varying vehicle count error
mpc_ql_error = [29.49078067, 31.41526384, 31.52831467, 31.64088214, 31.77035617]
mpc_qt_error = [25.88264626, 26.09637689, 26.14654485, 26.18363233, 26.20754507]
mpc_flow_error = [2157.6250000, 2129.7321429, 2129.9285714, 2128.9107143, 2129.3178571]

#cycle_times = ["No Error", "2% Error", "5% Error", "10% Error", "20% Error"]
#cycle_times = [15, 40, 65, 90]
#width = 9.5

plt.figure()

# Width of a bar 
cycle_times = np.array(cycle_times)

plt.bar(cycle_times, fixed_time_perf_flow, width, label="Fixed-time TSC")
#plt.bar(cycle_times, mpc_flow_error, color="r", label="MPC-based TSC")
plt.bar(cycle_times+width, mpc_based_perf_flow, width, color="tab:orange", label="MPC-based TSC")
plt.title("Comparison of Average Flow Rates for Similar Cycle Times")
plt.xlabel("Cycle Time (s)", fontsize=11)
plt.ylabel("Average Flow Rates (veh/hr)", fontsize=11)
#plt.xlim((65,163))
#plt.xlim((0,109.5))
plt.ylim((0,10500))
plt.xticks([70,80,90,100,154], rotation=0)
# First argument - A list of positions at which ticks should be placed
# Second argument -  A list of labels to place at the given locations
#plt.xticks(cycle_times + width / 2, ("Demand Profile 1", "Demand Profile 2", "Demand Profile 3", "Demand Profile 4"))
plt.legend()
#plt.legend(loc='best')
plt.gcf().autofmt_xdate()

plt.show()
