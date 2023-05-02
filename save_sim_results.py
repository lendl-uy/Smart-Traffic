# Author: Jan Lendl R. Uy
# CoE 199 Saving of Simulation Results for Each Time Step

# Write results of traffic simulation in separate text files

import os.path
import sys

directory = "results\\"

f = open(os.path.join(directory, "log.txt"), "r")

for num in f:
    last_run = int(num)

f.close()

new_run = str(last_run+1)

filename_u = f"mpc_green_times.txt"
filename_c = f"mpc_cycle.txt"
filename_veh_count = f"mpc_veh_count.txt"
filename_q_length = f"mpc_q_length.txt"
filename_q_time = f"mpc_q_time.txt"
filename_flow = f"mpc_flow.txt"
filename_sampled = f"mpc_sampled.txt"
filename_trajectory = f"mpc_trajectory.txt"
filename_final_results = f"mpc_final.txt"

filename_q_length = f"mpc_q_length.txt"
#filename_q_time = f"mpc_q_time.txt"
filename_flow = f"mpc_flow.txt"

step_len = 0.5
sim_duration = 50400 # Fixed

new_directory = os.path.join(directory, "test"+new_run)

try:
    os.mkdir(new_directory)
    f_u = open(os.path.join(new_directory, filename_u), "w")
    f_c = open(os.path.join(new_directory, filename_c), "w")
    f_vc = open(os.path.join(new_directory, filename_veh_count), "w")
    f_ql = open(os.path.join(new_directory, filename_q_length), "w")
    f_qt = open(os.path.join(new_directory, filename_q_time), "w")
    f_flow = open(os.path.join(new_directory, filename_flow), "w")
    f_trajectory = open(os.path.join(new_directory, filename_trajectory), "w")
    f_final = open(os.path.join(new_directory, filename_final_results), "w")
except:
    sys.exit(f"Cannot create a new directory! The directory {new_directory} already exists!")

def write_results_per_sec(veh_count, step, u = [61, 61, 45, 39, 87], C = 154):

    f_u.write(f"{step} {u[0]} {u[1]} {u[2]} {u[3]} {u[4]}\n")
    f_c.write(f"{step} {C}\n")
    f_vc.write(f"{step} {veh_count[0]} {veh_count[1]} {veh_count[2]} {veh_count[3]}\n")

    if step == sim_duration:
        try:
            f_u.close()
            f_c.close()
            f_vc.close()

            f = open(os.path.join(directory, "log.txt"), "w")
            f.write(f"{new_run}")
            f.close()
        except:
            print("Files have already been closed!")

def write_results_per_cycle(step, trajectory = [0, 0, 0, 0]):

    f_trajectory.write(f"{step}")
    for i in range(0, len(trajectory), 5):
        f_trajectory.write(f" {trajectory[i]} {trajectory[i+1]} {trajectory[i+2]} {trajectory[i+3]}")
    f_trajectory.write(f"\n")

    if step == sim_duration:
        try:
            f_trajectory.close()

            f = open(os.path.join(directory, "log.txt"), "w")
            f.write(f"{new_run}")
            f.close()
        except:
            print("The file has already been closed!")

def write_results_per_window(q_length, q_time, flow, step):

    f_ql.write(f"{step} {q_length}\n")
    f_qt.write(f"{step} {q_time}\n")
    f_flow.write(f"{step} {flow}\n")

    if step == sim_duration:
        try:
            f_vc.close()
            f_ql.close()
            f_qt.close()
            f_flow.close()
            f_trajectory.close()

            f = open(os.path.join(directory, "log.txt"), "w")
            f.write(f"{new_run}")
            f.close()
        except:
            print("Files have already been closed!")

def write_final_results(q_length, q_time, flow, step):

    f_final.write(f"{step} {q_length[0]} {q_length[1]} {q_length[2]} {q_length[3]} {q_length[4]}\n")
    f_final.write(f"{step} {q_time[0]} {q_time[1]} {q_time[2]} {q_time[3]} {q_time[4]}\n")
    f_final.write(f"{step} {flow[0]} {flow[1]} {flow[2]} {flow[3]} {flow[4]}\n")

    if step == sim_duration:
        try:
            f_final.close()

            f = open(os.path.join(directory, "log.txt"), "w")
            f.write(f"{new_run}")
            f.close()
        except:
            print("The file has already been closed!")