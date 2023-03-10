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

from mpc_params import *
import traffic_distribution as td

def do_mpc(x_curr=np.array([0,0,0,0]), step=0):

  # Initialize a model
  m = gp.Model("MPC")

  # Initialize GUROBI decision variables

  # x: vehicle count
  # u: green time
  x = m.addMVar(shape=(N+1,4), lb=xmin, vtype=GRB.INTEGER, name="x")
  u = m.addMVar(shape=(N,4), lb=umin, vtype=GRB.INTEGER, name="u")

  # C: cycle time
  # C_dummy: to be used for division
  C = m.addVar(vtype=GRB.INTEGER, lb=20.0, name="C")
  C_dummy = m.addVar(vtype=GRB.CONTINUOUS, name="C_dummy")

  # step: Current time step in the simulation
  # Used for generating a new vehicle distribution when an hour has elapsed
  t_step = int(step/T)

  d = np.array([[d_1p[t_step], d_2p[t_step], d_3p[t_step], d_4p[t_step]]])
  for i in range(t_step+1,t_step+N):
    d = np.concatenate((d, [[d_1p[i], d_2p[i], d_3p[i], d_4p[i]]]))
  D = d

  # u_41 and u_43 divides sum of green times in Aurora Blvd. East
  # Aurora Blvd. East has two phases, to Katipunan Ave. South and Aurora Blvd. West
  u_41 = m.addVar(vtype=GRB.INTEGER, lb=5.0, name="u_41")
  u_43 = m.addVar(vtype=GRB.INTEGER, lb=5.0, name="u_43")

  # Intermediary variables to compute difference of x(k+ko|ko) and u(k+ko|ko)
  y = m.addMVar(shape=(N+1,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="y") # x(k_o+k)-x(k_o)
  z = m.addMVar(shape=(N,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="z") # u(k_o+k)-u(k_o)

  # Constraints
  m.addConstr(x[0, :] == x_curr) # Initial number of vehicles
  for k in range(N):

    # Traffic model
    m.addConstr(x[k+1, :] == x[k, :] + u[k, :] @ B*C_dummy + D[k, :]) # (Bu(k))^T = u(k)^T B^T

    # Constraints in order to obey existing phases
    m.addConstr(u[k, 0] == u[k, 1]) # Green time of Katipunan Ave North and South must be the same
    m.addConstr(u[k, 3] == u_41+u_43) # Aurora East has 2 green times/phases
    m.addConstr(u[k, 2] == u_43-u_41-3) # Green time of Aurora West
    m.addConstr(C == u[k, 0] + u_43 + 6) # Total cycle time is equal to phase 1 + phase 2 + phase 3

    m.addConstr(C*C_dummy == 1) # To achieve same effect as 1/C
    m.addConstr(C <= 300)

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

  # Run MPC
  m.reset(0) # Clear previous results
  m.params.NonConvex = 2 # To allow division operator
  m.setParam('TimeLimit', 30) # 30s time limit
  m.feasRelaxS(0, True, False, False) # Ease model if infeasible
  m.optimize()

  # Obtain the results of the optimization
  names_to_retrieve = ["C", "u_41", "u_43"]
  vals = {}
  u_res = []

  # Only get values of u, x, and C
  for i in range(N):
    for j in range(4):
      names_to_retrieve.append(f"u[{i},{j}]")
      names_to_retrieve.append(f"x[{i},{j}]")

  if m.Status == GRB.INFEASIBLE:
    m.computeIIS() # Check for constraints leading to infeasibility
    m.write("iis.ilp")
  else:
    for v in m.getVars():
      if v.VarName in names_to_retrieve:
        vals[v.VarName] = v.X
        #print('%s %g' % (v.VarName, v.X))
        if v.VarName[:3] == "u[0" or (v.VarName == "u_41" or v.VarName == "u_43"):
          u_res.append(v.X)

    # Post-processing of data
    for i in range(len(u_res)):
      if u_res[i] < 0:
        print(f"Negative green time detected!")
        break
      u_res[i] = int(u_res[i]+0.5) # Convert to integer

    vals['C'] = int(vals['C']+0.5) # Convert to integer

    #print(f"xmin = {xmin}")
    #print(f"xmax = {xmax}")
    #print(f"umin = {umin}")
    #print(f"umax = {umax}")
    #print(f"B = {B}")
    #print(f"D = {D}")
    #print(f"Q = {Q}")
    #print(f"R = {R}")

    return u_res, vals['C']
  
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
  u, C = do_mpc()
  print(f"u[0,:] = {u}")
  print(f"C = {C}")
  get_timer_settings(u, C)

if __name__ == "__main__":
  main()
