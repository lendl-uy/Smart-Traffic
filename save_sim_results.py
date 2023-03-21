# Write results of traffic simulation in 4 separate text files

import os.path
import shutil

directory = "results\\"

f = open(os.path.join(directory, "log.txt"), "r")

for num in f:
    last_run = int(num)

new_run = str(last_run+1)

filename_u = f"mpc_green_times.txt"
filename_c = f"mpc_cycle.txt"
filename_veh_count = f"mpc_veh_count.txt"
filename_q_length = f"mpc_q_length.txt"
filename_q_time = f"mpc_q_time.txt"
filename_flow = f"mpc_flow.txt"
filename_spawned = f"mpc_spawned.txt"

duration = 50400

new_directory = os.path.join(directory, "test"+new_run)

try:
    os.mkdir(new_directory)
except:
    shutil.rmtree(new_directory, ignore_errors=True)
    os.rmdir(new_directory)

f_u = open(os.path.join(new_directory, filename_u), "w")
f_c = open(os.path.join(new_directory, filename_c), "w")
f_vc = open(os.path.join(new_directory, filename_veh_count), "w")
f_ql = open(os.path.join(new_directory, filename_q_length), "w")
f_qt = open(os.path.join(new_directory, filename_q_time), "w")
f_flow = open(os.path.join(new_directory, filename_flow), "w")
f_spawned = open(os.path.join(new_directory, filename_spawned), "w")

def write_results(veh_count, q_length, q_time, flow, spawned, step, u = [61, 61, 45, 39, 87], C = 154):

    f_u.write(f"{step} {u[0]} {u[1]} {u[2]} {u[3]} {u[4]}\n")
    f_c.write(f"{step} {C}\n")
    f_vc.write(f"{step} {veh_count[0]} {veh_count[1]} {veh_count[2]} {veh_count[3]}\n")
    f_ql.write(f"{step} {q_length[0]} {q_length[1]} {q_length[2]} {q_length[3]}\n")
    f_qt.write(f"{step} {q_time[0]} {q_time[1]} {q_time[2]} {q_time[3]}\n")
    f_flow.write(f"{step} {flow[0]} {flow[1]} {flow[2]} {flow[3]}\n")
    f_spawned.write(f"{step} {spawned[0]} {spawned[1]} {spawned[2]} {spawned[3]}\n")

    if step==duration-1:
        f_vc.close()
        f_ql.close()
        f_qt.close()
        f_flow.close()
        f_spawned.close()
        f = open(os.path.join(directory, "log.txt"), "w")
        f.write(f"{new_run}")
        f.close()
        