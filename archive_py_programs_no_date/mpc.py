# Author: Jan Lendl R. Uy
# CoE 199 MPC Implementation using GUROBI

# Conventions
# Subscript 1: Katipunan Ave South
# Subscript 2: Katipunan Ave North
# Subscript 3: Aurora Blvd West
# Subscript 4: Aurora Blvd East

# Tags (enclosed in parentheses)
# DUMMY: Temp values for initial testing
# TUNABLE: To be tuned during Testing Phase

import gurobipy as gp
from gurobipy import GRB

import numpy as np
import math

from mpc_params import *

def do_mpc(x_curr=np.array([50, 30, 20, 10]), step=0):

    # Initialize a model
    m = gp.Model("MPC")

    # Disable printing of log information in console
    m.Params.LogToConsole = 0

    # Initialize GUROBI decision variables

    # x: vehicle count
    # u: green time
    x = m.addMVar(shape=(N+1,4), lb=xmin, vtype=GRB.CONTINUOUS, name="x")
    u = m.addMVar(shape=(N,4), lb=umin, vtype=GRB.INTEGER, name="u")

    # C: cycle time
    # C_dummy: to be used for division
    #C = 300
    C = m.addVar(vtype=GRB.INTEGER, lb=C_min, ub = C_max, name="C")
    C_dummy = m.addVar(vtype=GRB.CONTINUOUS, name="C_dummy")

    # step: Current time step in the simulation
    # Used for generating a new vehicle distribution when an hour has elapsed
    t_step = int(step/T)

    d = np.array([[d_1p[t_step], d_2p[t_step], d_3p[t_step], d_4p[t_step]]])
    for i in range(t_step+1,t_step+N):
        # Pad zeros for instances when time approaches 8PM and matrix cuts are uneven
        #if i < len(d_1p):
        if i < d_1p.size:
            d = np.concatenate((d, [[d_1p[i], d_2p[i], d_3p[i], d_4p[i]]]))
        else:
            d = np.concatenate((d, [[0.0, 0.0, 0.0, 0.0]]))
    D = d
    #print(f"D = {D}")

    # Obtain the proportionality constant between Aurora East to West and Aurora East to Katipunan South
    d_41 = np.array(d_41p[t_step:t_step+N])
    d_4mult = []
    max_multiplier = math.floor((C_max-L)/u_min_val)

    # Pad zeros if there are insufficient entries
    if d_41.size < N:
        temp = d_41
        remaining_entries = int(N-temp.size)
        d_41 = np.append(temp, np.zeros(remaining_entries, dtype=float))

    # Obtain multiplier for Aurora East to Katipunan South green time
    for i in range(N):

        if d_41[i] > 0.0:
            d_4mult_entry = round(D[i,3]/d_41[i])
        else:
           d_4mult_entry = D[i,3]

        if d_4mult_entry > math.floor(max_multiplier/2):
            d_4mult_entry = math.floor(max_multiplier/2)

        d_4mult.append(d_4mult_entry)

    if sum(d_4mult) <= 0.0:
        u_41mult = 1
    else:
        u_41mult = int(sum(d_4mult)/len(d_4mult)+0.5)

    # Obtain constraints for green times to speed up GUROBI convergence
    # Compute constraints in terms of demand OR current vehicle count
    if x_curr[0] < x_curr[1]:
        x_total = np.sum(x_curr[1:])
    else:
        x_total = x_curr[0]+np.sum(x_curr[2:])

    d_sum = np.sum(D[0:,1:], axis=0)
    d_total = np.sum(d_sum)
    max_multiplier = math.floor((C_max-L)/u_min_val)

    if sum(x_curr) <= 0.0:
        u_2mult = max_multiplier*(d_sum[0]/d_total)
        u_3mult = max_multiplier*(d_sum[1]/d_total)
        u_4mult = max_multiplier*(d_sum[2]/d_total)
    else:
        if x_curr[0] < x_curr[1]:
            u_2mult = max_multiplier*(x_curr[1]/x_total)
        else:
            u_2mult = max_multiplier*(x_curr[0]/x_total)
        u_3mult = max_multiplier*(x_curr[2]/x_total)
        u_4mult = max_multiplier*(x_curr[3]/x_total)

    u_2max = round(u_min_val*u_2mult)
    u_3max = round(u_min_val*u_3mult)
    u_4max = round(u_min_val*u_4mult)

    #print(f"u_2max = {u_2max}")
    #print(f"u_3max = {u_3max}")
    #print(f"u_4max = {u_4max}")

    # Add error to the measurement of vehicles based on error constant
    '''
    for i in range(len(x_curr)):
        error_delta = x_curr[i]*error/2
        num_random = np.random.randint(x_curr[i]-error_delta, x_curr[i]+error_delta+1)
        x_curr[i] = num_random
    '''
    # u_41 and u_43 divides sum of green times in Aurora Blvd. East
    # Aurora Blvd. East has two phases, to Katipunan Ave. South and Aurora Blvd. West
    u_41 = m.addVar(vtype=GRB.INTEGER, lb=u_min_val, name="u_41")
    u_43 = m.addVar(vtype=GRB.INTEGER, lb=u_min_val, name="u_43")

    # Intermediary variables to compute difference of x(k+ko|ko) and u(k+ko|ko)
    y = m.addMVar(shape=(N+1,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="y") # x(k_o+k)-x(k_o)
    z = m.addMVar(shape=(N,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="z") # u(k_o+k)-u(k_o)

    # Constraints
    m.addConstr(x[0, :] == x_curr) # Initial number of vehicles
    print(f"x_curr = {x_curr}")
    for k in range(N):

        # Traffic model
        m.addConstr(x[k+1, :] == x[k, :] + u[k, :] @ B*C_dummy + D[k, :]) # (Bu(k))^T = u(k)^T B^T
        #m.addConstr(x[k+1, :] == x[k, :] + u[k, :] @ B + D[k, :]) # (Bu(k))^T = u(k)^T B^T

        # Constraints in order to obey existing phases
        m.addConstr(u[k, 0] == u[k, 1]) # Green time of Katipunan Ave North and South must be the same
        m.addConstr(u[k, 3] == u_41+u_43) # Aurora East has 2 green times/phases
        m.addConstr(u[k, 2] == u_43-u_41-3) # Green time of Aurora West
        #m.addConstr(C == u[k, 0] + u_43 + 6) # Total cycle time is equal to phase 1 + phase 2 + phase 3 + lost time
        m.addConstr(C == u[k, 0] + u_41 + u[k, 2] + 9) # Total cycle time is equal to phase 1 + phase 2 + phase 3 + lost time

        # EXPERIMENTAL
        m.addConstr(u_43 >= u_41*u_41mult) # Green time constraint of Aurora East to West
        m.addConstr(u[k, 0] >= u_2max) # Green time constraint of Katipunan South and North
        m.addConstr(u[k, 0] >= u[k, 2]) # Green time constraint of Katipunan South and North
        m.addConstr(u[k, 2] >= u_3max) # Green time constraint of Aurora West
        m.addConstr(u[k, 2] >= u_41) # Green time constraint of Aurora West
        m.addConstr(u[k, 3] >= u_4max) # Green time constraint of Aurora East

        #m.addConstr(u[k, 0] >= u_41*u_2mult) # Green time constraint of Aurora East to West
        #m.addConstr(u[k, 2] <= u_41*u_3mult) # Green time constraint of Aurora East to West
        #m.addConstr(u[k, 3] >= u_41*u_4mult) # Green time constraint of Aurora East to West
        #m.addConstr(u_41 >= u_min_val) # Green time constraint of Aurora East to West

        #m.addConstr(u_43 >= u_41*3) # Green time constraint of Aurora East to West
        #m.addConstr(u[k, 0] >= u_41*3) # Green time constraint of Katipunan South and North
        #m.addConstr(u[k, 2] <= u[k, 0]-5) # Green time constraint of Aurora West
        #m.addConstr(u[k, 0] >= u_41*2) # Green time constraint of Katipunan South and North
        #m.addConstr(u[k, 2] >= u_41*2) # Green time constraint of Aurora West

        m.addConstr(C*C_dummy == 1) # To achieve same effect as 1/C

        # Intermediate variable to compute Q and R norm
        #m.addConstr(y[k, :] == x[k, :] - x[0, :])
        m.addConstr(y[k, :] == x[k, :] - xref)
        m.addConstr(z[k, :] == u[k, :] - u[0, :])
    #m.addConstr(y[N, :] == x[N, :] - x[0, :])
    m.addConstr(y[N, :] == x[N, :] - xref)

    # Objective function
    # Note: Transposition is automatically handled by GUROBI
    obj1 = sum(y[k, :] @ Q @ y[k, :] for k in range(N+1))
    obj2 = sum(z[k, :] @ R @ z[k, :] for k in range(N))
    obj = obj1 + obj2

    # Set objective function
    m.setObjective(obj, GRB.MINIMIZE)

    # Check for infeasibility / unboundedness
    m.setParam("DualReductions", 0) # Infeasible model check

    # Save the model
    m.write("mpc.lp")

    # Run MPC
    m.reset(0) # Clear previous results
    m.params.NonConvex = 2 # To allow division operator
    m.setParam('TimeLimit', 2) # 30s time limit
    #m.feasRelaxS(1, True, True, False) # Ease model if infeasible
    m.optimize()

    # Obtain the results of the optimization
    names_to_retrieve = ["C", "u_41", "u_43"]
    vals = {}
    u_res = []
    #relaxed = 0

    x_trajectory = []

    # Only get values of u, x, and C
    for i in range(N):
        for j in range(4):
            names_to_retrieve.append(f"u[{i},{j}]")
            names_to_retrieve.append(f"x[{i},{j}]")

    for j in range(4):
        names_to_retrieve.append(f"x[{N},{j}]")

    if m.Status == GRB.INFEASIBLE:
        print("Model is infeasible!")
        m.computeIIS() # Check for constraints leading to infeasibility
        m.write("iis.ilp")
        m.feasRelaxS(1, True, True, False) # Ease model if infeasible
        m.optimize()
        #relaxed = 1
        for v in m.getVars():
            if v.VarName in names_to_retrieve:
                vals[v.VarName] = v.X
                #print('%s %g' % (v.VarName, v.X))
                if v.VarName[:3] == "u[0" or (v.VarName == "u_41" or v.VarName == "u_43"):
                    u_res.append(v.X)
                elif v.VarName[:1] == "x":
                    x_trajectory.append(int(v.X+0.5))
    else:
        for v in m.getVars():
            if v.VarName in names_to_retrieve:
                vals[v.VarName] = v.X
                #print('%s %g' % (v.VarName, v.X))
                if v.VarName[:3] == "u[0" or (v.VarName == "u_41" or v.VarName == "u_43"):
                    u_res.append(v.X)
                elif v.VarName[:1] == "x":
                    x_trajectory.append(int(v.X+0.5))

    # Post-processing of data
    additive = []
    for i in range(len(u_res)):
        u_res[i] = int(u_res[i]+0.5) # Convert to integer
        print(f"u_res = {u_res[i]}")
        if u_res[i] < u_min_val:
            additive.append(u_min_val-(u_res[i])) # Dummy additive to reach minimum green time of 15s
            print("Model was relaxed")
            continue

    if len(additive) > 0:
        additional_time = max(additive)
        for i in range(len(u_res)):
            u_res[i] += additional_time
        
    proc_C = int((u_res[0]+u_res[4]+u_res[2]+9)+0.5)# Convert to integer

    #print(f"xmin = {xmin}")
    #print(f"xmax = {xmax}")
    #print(f"umin = {umin}")
    #print(f"umax = {umax}")
    #print(f"B = {B}")
    #print(f"D = {D}")
    #print(f"Q = {Q}")
    #print(f"R = {R}")

    return u_res, proc_C, x_trajectory

def get_timer_settings(u, C):
  
    # Amber time (3s, fixed)
    A = 3
    
    # Green times of relevant roads
    u_katip_s = u[0] # Green time for Katipunan South for phase 1
    u_katip_n = u[1] # Green time for Katipunan North for phase 1
    u_aurora_w = u[2] # Green time of Aurora West for phase 3
    u_aurora_e_katip_s = u[4] # Green time of Aurora East for phase 2
    u_aurora_e_aurora_w = u[5] # Green time of Aurora East for phase 3

    u_sorted = [u_katip_s, u_katip_n, u_aurora_w, u_aurora_e_katip_s, u_aurora_e_aurora_w]
    
    phase_1 = 0
    phase_2 = u_katip_s + A
    phase_3 = u_katip_s + u_aurora_e_katip_s + 2*A

    phases = [phase_1, phase_2, phase_3]

    return u_sorted, phases
  
def main():
    u, C, trajectory = do_mpc()
    print(f"u[0,:] = {u}")
    print(f"C = {C}")
    print(f"trajectory = {trajectory}")
    print(f"len trajectory = {len(trajectory)}")
    get_timer_settings(u, C)

if __name__ == "__main__":
    main()