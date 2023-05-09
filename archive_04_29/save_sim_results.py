# Author: Jan Lendl R. Uy
# CoE 199 Saving of Simulation Results for Each Time Step

# Write results of traffic simulation in separate text files

import os.path

directory = "results\\"

f = open(os.path.join(directory, "log.txt"), "r")

for num in f:
    last_run = int(num)

new_run = str(last_run+1)

filename_u = f"mpc_green_times.txt"
filename_c = f"mpc_cycle.txt"
filename_veh_count = f"mpc_veh_count.txt"
filename_q_length_cumul = f"mpc_q_length_cumulative.txt"
filename_q_time_cumul = f"mpc_q_time_cumulative.txt"
filename_flow_cumul = f"mpc_flow_cumulative.txt"
filename_spawned = f"mpc_spawned.txt"
filename_sampled = f"mpc_sampled.txt"
filename_trajectory = f"mpc_trajectory.txt"

filename_q_length = f"mpc_q_length.txt"
#filename_q_time = f"mpc_q_time.txt"
filename_flow = f"mpc_flow.txt"

step_len = 0.5
duration = 50400 # Fixed

new_directory = os.path.join(directory, "test"+new_run)

try:
    os.mkdir(new_directory)
except:
    print(f"Cannot create a new directory! The directory {new_directory} already exists!")

f_u = open(os.path.join(new_directory, filename_u), "w")
f_c = open(os.path.join(new_directory, filename_c), "w")
f_vc = open(os.path.join(new_directory, filename_veh_count), "w")
f_ql = open(os.path.join(new_directory, filename_q_length_cumul), "w")
f_qt = open(os.path.join(new_directory, filename_q_time_cumul), "w")
f_flow = open(os.path.join(new_directory, filename_flow_cumul), "w")
f_sampled = open(os.path.join(new_directory, filename_sampled), "w")
f_trajectory = open(os.path.join(new_directory, filename_trajectory), "w")

def write_results_per_sec(veh_count, q_length, q_time, flow, spawned, step, u = [61, 61, 45, 39, 87], C = 154):

    f_u.write(f"{step} {u[0]} {u[1]} {u[2]} {u[3]} {u[4]}\n")
    f_c.write(f"{step} {C}\n")
    f_vc.write(f"{step} {veh_count[0]} {veh_count[1]} {veh_count[2]} {veh_count[3]}\n")
    f_ql.write(f"{step} {q_length[0]} {q_length[1]} {q_length[2]} {q_length[3]}\n")
    f_qt.write(f"{step} {q_time[0]} {q_time[1]} {q_time[2]} {q_time[3]}\n")
    f_flow.write(f"{step} {flow[0]} {flow[1]} {flow[2]} {flow[3]}\n")

    if step==duration:
        f_vc.close()
        f_ql.close()
        f_qt.close()
        f_flow.close()
        f_sampled.close()
        f_trajectory.close()
        f = open(os.path.join(directory, "log.txt"), "w")
        f.write(f"{new_run}")
        f.close()

def write_results_per_cycle(step, sampled = [0, 0, 0, 0], trajectory = [0, 0, 0, 0]):

    f_sampled.write(f"{step} {sampled[0]} {sampled[1]} {sampled[2]} {sampled[3]}\n")

    f_trajectory.write(f"{step}")
    for i in range(0, len(trajectory), 4):
        f_trajectory.write(f" {trajectory[i]} {trajectory[i+1]} {trajectory[i+2]} {trajectory[i+3]}")
    f_trajectory.write(f"\n")

    if step==duration:
        f_vc.close()
        f_ql.close()
        f_qt.close()
        f_flow.close()
        f_sampled.close()
        f_trajectory.close()
        f = open(os.path.join(directory, "log.txt"), "w")
        f.write(f"{new_run}")
        f.close()