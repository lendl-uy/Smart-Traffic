# Author: Jan Lendl R. Uy
# CoE 199 MPC Implementation using GUROBI

# Conventions
# Subscript 1: Katipunan Ave South
# Subscript 2: Katipunan Ave North
# Subscript 3: Aurora Blvd West
# Subscript 4: Aurora Blvd East / Aurora Blvd East to West

# Tags (enclosed in parentheses)
# DUMMY: Temp values for initial testing
# TUNABLE: To be tuned during Testing Phase

import gurobipy as gp
from gurobipy import GRB

import numpy as np
import math
import sys

from mpc_params import *

def get_weighted_u_min(veh_count, D, u_min):

    # Obtain constraints for green times to speed up GUROBI convergence
    # Compute constraints in terms of demand OR current vehicle count

    x_total = np.sum(veh_count[:-1])

    d_sum_katip = np.sum(D[:,:2], axis=1)
    d_sum_aurora = np.sum(D[:,2:], axis=0)
    d_total_katip = np.sum(d_sum_katip)
    d_total_aurora = np.sum(d_sum_aurora)
    d_total = d_total_katip+d_total_aurora

    max_multiplier = math.floor((C-L)/(u_min*1.25))

    if sum(veh_count) <= 0.0:
        u_1mult = max_multiplier*(d_total_katip/d_total)
        u_3mult = max_multiplier*(d_sum_aurora[0]/d_total)
        u_43mult = max_multiplier*(d_sum_aurora[1]/d_total)
        u_41mult = min(u_1mult, u_3mult, u_43mult, 1)
    else:
        u_1mult = max_multiplier*((veh_count[0]+veh_count[1])/x_total)
        u_3mult = max_multiplier*(veh_count[2]/x_total)
        u_43mult = max_multiplier*((veh_count[3]-veh_count[4])/x_total)
        u_41mult = max_multiplier*(veh_count[4]/x_total)

    u_1min = round(u_min*u_1mult)
    u_3min = round(u_min*u_3mult)
    u_43min = round(u_min*u_43mult)
    u_41min = round(u_min*u_41mult)

    return u_1min, u_3min, u_43min, u_41min

def construct_demand_mtx(d_1, d_2, d_3, d_43, d_41, C, step):

    t_step = int(step/3600)

    d = np.array([[d_1[t_step], d_2[t_step], d_3[t_step], d_43[t_step], d_41[t_step]]])
    for i in range(N):
        t_step = int((step+i*C)/3600)

        # Pad zeros for instances when time approaches 8PM and matrix cuts are uneven
        if t_step < len(d_1):
        #if i < d_1p.size:
            d = np.concatenate((d, [[d_1[t_step], d_2[t_step], d_3[t_step], d_43[t_step], d_41[t_step]]]))
        else:
            d = np.concatenate((d, [[0.0, 0.0, 0.0, 0.0, 0.0]]))
    D = C*d

    return D

def apply_u_additive(array, min_val):

    array_proc = []
    for i in range(len(array)):
        array[i] = int(array[i]+0.5) # Convert entry to integer
        if array[i] < min_val:
            array_proc.append(min_val-(array[i])) # Store additive in an array to find maximum

    # Apply maximum additive to all entries
    if len(array_proc) > 0:
        additional_time = max(array_proc)
        for i in range(len(array)):
            array[i] += additional_time

    return array

def do_mpc(x_curr=np.array([16, 91, 20, 68, 14]), step=12459):

    # Initialize a model
    m = gp.Model("MPC")

    # GUROBI PARAMETERS
    # 1st line: Disable printing of log information in console
    # 2nd line: Discard previous solutions to not affect new MPC run
    # 3rd line: Set maximum runtime of MPC to 2 seconds
    m.Params.LogToConsole = 0
    m.reset(0)
    m.setParam('TimeLimit', 2)

    # INITIALIZATION OF GUROBI DECISION VARIABLES

    # x: vehicle count
    # u: green time
    x = m.addMVar(shape=(N+1,5), lb=xmin, ub=xmax, vtype=GRB.CONTINUOUS, name="x")
    u = m.addMVar(shape=(N,5), lb=umin, vtype=GRB.INTEGER, name="u")

    # step: Current time step in the simulation
    # Used for checking new demand when an hour has elapsed
    t_step = int(step/3600)

    # Construct the demand matrix based on the current hour
    D = construct_demand_mtx(d_1, d_2, d_3, d_43, d_41, C, step)
    print(f"D = {D}")

    # Obtain the proportionality constant between Aurora East to West and Aurora East to Katipunan South
    t_step = int(step/3600)
    d_41prop = np.array(d_41[t_step:t_step+N])
    d_4mult = []
    max_multiplier = math.floor((C-L)/(u_min_val))

    # Pad zeros if there are insufficient entries
    if d_41prop.size < N:
        temp = d_41prop
        remaining_entries = int(N-temp.size)
        d_41prop = np.append(temp, np.zeros(remaining_entries, dtype=float))

    # Obtain multiplier for Aurora East to Katipunan South green time
    for i in range(N):

        if d_41prop[i] > 0.0:
            d_4mult_entry = round(D[i,3]/d_41prop[i])
        else:
            d_4mult_entry = D[i,3]

        if d_4mult_entry > math.floor(max_multiplier/2):
            d_4mult_entry = math.floor(max_multiplier/2)

        d_4mult.append(d_4mult_entry)

    if sum(d_4mult) <= 0.0:
        u_41mult = 1
    else:
        u_41mult = int(sum(d_4mult)/len(d_4mult)+0.5)

    # Get weighted minimum green times
    u_1min, u_3min, u_43min, u_41min = get_weighted_u_min(x_curr, D, u_min_val)

    print(f"u_1min = {u_1min}")
    print(f"u_3min = {u_3min}")
    print(f"u_43min = {u_43min}")
    print(f"u_41min = {u_41min}")
    
    # Add error to the measurement of vehicles based on error constant
    '''
    for i in range(len(x_curr)):
        error_delta = x_curr[i]*error/2
        num_random = np.random.randint(x_curr[i]-error_delta, x_curr[i]+error_delta+1)
        x_curr[i] = num_random
    '''

    # Intermediary variables to compute difference of x(k+ko|ko) and u(k+ko|ko)
    y = m.addMVar(shape=(N+1,5), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="y") # x(k_o+k)-x(k_o)
    z = m.addMVar(shape=(N,5), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="z") # u(k_o+k)-u(k_o)

    # MPC MODEL CONSTRAINTS

    # Set the initial vehicle count to the measured number of vehicles
    m.addConstr(x[0, :] == x_curr)
    print(f"x_curr = {x_curr}")

    for k in range(N):

        # Traffic model
        m.addConstr(x[k+1, :] == x[k, :] + u[k, :] @ B + D[k, :]) # (Bu(k))^T = u(k)^T B^T

        # Constraints in order to obey existing phases
        m.addConstr(u[k, 0] == u[k, 1]) # Green time of Katipunan Ave North and South must be the same
        #m.addConstr(u[k, 2] == u[k, 3]-u[k, 4]-3) # Green time of Aurora West
        #m.addConstr(C == u[k, 0] + u[k, 4] + u[k, 2] + 9) # Total cycle time is equal to phase 1 + phase 2 + phase 3 + lost time

    
        # Skip phase 2 if Aurora East to West is less than half of u_min_val
        if u_41min <= (u_min_val-1)/4:
            m.addConstr(u[0, 4] == 0)
            m.addConstr(u[0, 2] == u[0, 3]) # Phase 2 is skipped altogether
            m.addConstr(C == u[k, 0] + u[k, 2] + 6) # Total cycle time is equal to phase 1 + phase 3 + lost time
        else:
            m.addConstr(u[k, 2] == u[k, 3]-u[k, 4]-3) # Green time of Aurora West
            m.addConstr(C == u[k, 0] + u[k, 4] + u[k, 2] + 9) # Total cycle time is equal to phase 1 + phase 2 + phase 3 + lost time
        
        # Intermediate variable to compute Q and R norm
        m.addConstr(y[k, :] == x[k, :] - xref)
        m.addConstr(z[k, :] == u[k, :] - u[0, :])

    m.addConstr(y[N, :] == x[N, :] - xref)

    # EXPERIMENTAL
    # Set next set of green times such that based on the current vehicle count
    #m.addConstr(u[0, 3] >= u[0, 4]*u_41mult) # Green time constraint of Aurora East to West
    m.addConstr(u[0, 0] >= u_1min) # Green time constraint of Katipunan South and North
    m.addConstr(u[0, 2] >= u_3min) # Green time constraint of Aurora West
    m.addConstr(u[0, 2] >= u[0, 4]) # Green time constraint of Aurora West
    m.addConstr(u[0, 3] >= u_43min) # Green time constraint of Aurora East
    
    if u_1min >= u_3min:
        m.addConstr(u[0, 0] >= u[0, 2]) # Green time constraint of Katipunan South and North
    else:
        m.addConstr(u[0, 2] >= u[0, 0]) # Green time constraint of Aurora West

    if (u_41min < u_min_val) and (u_41min >= (u_min_val-1)/4):
        m.addConstr(u[0, 4] == u_min_val)
    
    if u_41min < (u_min_val-1)/4:
        m.addConstr(u[0, 4] == 0)

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
    m.optimize()

    # Obtain the results of the optimization
    names_to_retrieve = ["C"]
    vals = {}
    u_res = []
    relaxed = 0

    x_trajectory = []

    # Only get values of u, x
    for i in range(N):
        for j in range(5):
            names_to_retrieve.append(f"u[{i},{j}]")
            names_to_retrieve.append(f"x[{i},{j}]")

    for j in range(5):
        names_to_retrieve.append(f"x[{N},{j}]")

    if m.Status == GRB.INFEASIBLE:
        print("Model is infeasible!")
        m.computeIIS() # Check for constraints leading to infeasibility
        m.write("iis.ilp")

        m.feasRelaxS(0, True, True, False) # Ease model if infeasible
        m.optimize()

        if m.Status == GRB.INFEASIBLE:
            print("Cannot find optimal green times!")
            sys.exit("Exiting the program now.")

        relaxed += 1

        # Retrieve the computed green times and predicted future states
        for v in m.getVars():
            if v.VarName in names_to_retrieve:
                vals[v.VarName] = v.X
                #print('%s %g' % (v.VarName, v.X))
                if v.VarName[:3] == "u[0":
                    u_res.append(v.X)
                elif v.VarName[:1] == "x":
                    x_trajectory.append(int(v.X+0.5))
    else:
        # Retrieve the computed green times and predicted future states
        for v in m.getVars():
            if v.VarName in names_to_retrieve:
                vals[v.VarName] = v.X
                #print('%s %g' % (v.VarName, v.X))
                if v.VarName[:3] == "u[0":
                    u_res.append(v.X)
                elif v.VarName[:1] == "x":
                    x_trajectory.append(int(v.X+0.5))
    
    # Post-processing of data
    u_res = apply_u_additive(u_res, 0)

    if u_41min <= (u_min_val-1)/4:
        final_C = int((u_res[0]+u_res[2]+6)+0.5) # Convert to integer
    else:
        final_C = int((u_res[0]+u_res[4]+u_res[2]+9)+0.5) # Convert to integer
    
    return u_res, final_C, x_trajectory, relaxed

def get_timer_settings(u, C):
  
    # Amber time (3s, fixed)
    A = 3
    
    # Green times of relevant roads
    u_katip_s = u[0] # Green time for Katipunan South for phase 1
    u_katip_n = u[1] # Green time for Katipunan North for phase 1
    u_aurora_w = u[2] # Green time of Aurora West for phase 3
    u_aurora_e_aurora_w = u[3] # Green time of Aurora East for phase 3
    u_aurora_e_katip_s = u[4] # Green time of Aurora East for phase 2

    u_sorted = [u_katip_s, u_katip_n, u_aurora_w, u_aurora_e_katip_s, u_aurora_e_aurora_w]
    
    phase_1 = 0
    phase_2 = u_katip_s + A
    phase_3 = u_katip_s + u_aurora_e_katip_s + 2*A

    if u_aurora_e_katip_s > 0:
        phases = [phase_1, phase_2, phase_3]
    else:
        phases = [phase_1, phase_2, phase_3]

    return u_sorted, phases

def phase_2_skipped(phases):

    if phases[2]-3 == phases[1]:
        return True
    return False

def main():
    u, C, trajectory, relaxed = do_mpc()
    u_sorted, phases = get_timer_settings(u, C)
    print(f"C = {C}")
    print(f"u_sorted = {u_sorted}")
    print(f"phases = {phases}")
    #print(f"trajectory = {trajectory}")

if __name__ == "__main__":
    main()