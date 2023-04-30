import gurobipy as gp
from gurobipy import GRB

import numpy as np
import scipy.sparse as sp

from read_dua_demand import create_dua_demand

# Create a new model
m = gp.Model("MPC")

# horizon
N = 5 # (TUNABLE)
u_min_val = 15 # (TUNABLE)
C_min = 50 # (TUNABLE)
C_max = 150 # (TUNABLE)
step = 0

# Traffic model variables (s)
T = 150 # Control interval (must divide 3600 w/out decimal)
L = 9  # Lost time (3 phases * 3s)

# Saturation flow rate (veh/hr -> veh/s)
S_1 = 841*(1/3600) # Saturation flow
S_2 = 1510*(1/3600) # Saturation flow
S_3 = 2017*(1/3600) # Saturation flow
S_4 = 3191*(1/3600) # Saturation flow

# Bounds
xmin = np.array([0,0,0,0])
xref = np.array([0,0,0,0]) # (TUNABLE)
umin = np.array([u_min_val,u_min_val,u_min_val,u_min_val]) # Cannot have a zero timer setting

# Create variables
xmin = np.tile(xmin, (N+1,1))
umin = np.tile(umin, (N,1))

x = m.addMVar(shape=(N+1,4), lb=xmin, vtype=GRB.CONTINUOUS, name='x')
u = m.addMVar(shape=(N,4), lb=umin, vtype=GRB.INTEGER, name='u')
y = m.addMVar(shape=(N+1,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="y") # x(k_o+k)-x(k_o)
z = m.addMVar(shape=(N,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="z") # u(k_o+k)-u(k_o)

# u_41 and u_43 divides sum of green times in Aurora Blvd. East
# Aurora Blvd. East has two phases, to Katipunan Ave. South and Aurora Blvd. West
u_41 = m.addVar(vtype=GRB.INTEGER, lb=u_min_val, name="u_41")
u_43 = m.addVar(vtype=GRB.INTEGER, lb=u_min_val, name="u_43")

C = m.addVar(vtype=GRB.INTEGER, lb=C_min, ub = C_max, name="C")
C_dummy = m.addVar(vtype=GRB.CONTINUOUS, name="C_dummy")

# B contains the road link properties
B = np.array([[S_1,0,0,0],
              [0,S_2,0,0],
              [0,0,S_3,0],
              [0,0,0,S_4]
              ])
B = -T*B

try:
    d_1p, d_2p, d_3p, d_4p = create_dua_demand(T, 50400, "sumo\\micro\\003\\tripinfo_003.xml")
except:
    print(f"Error in creatind dua demand!")

# step: Current time step in the simulation
# Used for generating a new vehicle distribution when an hour has elapsed
t_step = int(step/T)

d = np.array([[d_1p[t_step], d_2p[t_step], d_3p[t_step], d_4p[t_step]]])
for i in range(t_step+1,t_step+N):
    # Pad zeros for instances when time approaches 8PM and matrix cuts are uneven
    if i < d_1p.size:
        d = np.concatenate((d, [[d_1p[i], d_2p[i], d_3p[i], d_4p[i]]]))
    else:
        d = np.concatenate((d, [[0.0, 0.0, 0.0, 0.0]]))
D = d
print(f"D = {D}")

# Weighting matrix W (traffic volume penalization)
w_1 = 1/((960)**2)
w_2 = 1/((2661)**2)
w_3 = 1/((3312)**2)
w_4 = 1/((1137)**2)
Q = np.array([[w_1,0,0,0],
              [0,w_2,0,0],
              [0,0,w_3,0],
              [0,0,0,w_4]
              ])

# Weighting matrix R (control input penalization)
r_1 = 0.05 # (TUNABLE)
r_2 = 0.1 # (TUNABLE)
r_3 = 0.25 # (TUNABLE)
r_4 = 0.25 # (TUNABLE)
R = np.array([[r_1,0,0,0],
              [0,r_2,0,0],
              [0,0,r_3,0],
              [0,0,0,r_4]
              ])

# MPC Formulation
m.addConstr(x[0, :] == np.zeros(4))
for k in range(N):
    m.addConstr(x[k+1, :] == x[k, :] + u[k, :] @ B * C_dummy + D[k, :]) # (Bu(k))^T = u(k)^T B^T
    m.addConstr(C*C_dummy == 1) # To achieve same effect as 1/C
    m.addConstr(y[k, :] == x[k, :] - xref)
    m.addConstr(z[k, :] == u[k, :] - u[0, :])
    m.addConstr(u[k, 0] == u[k, 1]) # Green time of Katipunan Ave North and South must be the same
    m.addConstr(u[k, 3] == u_41+u_43) # Aurora East has 2 green times/phases
    m.addConstr(u[k, 2] == u_43-u_41-3) # Green time of Aurora West
    m.addConstr(u[k, 2] >= u_41) # Green time of Aurora West must be greater than or equal to green time of Aurora East to Katipunan South
    m.addConstr(C == u[k, 0] + u_41 + u[k, 2] + 9) # Total cycle time is equal to phase 1 + phase 2 + phase 3 + lost time
m.addConstr(y[N, :] == x[N, :] - xref)

# Objective function
# Note: Transposition is automatically handled by GUROBI
obj1 = sum(y[k, :] @ Q @ y[k, :] for k in range(N+1))
obj2 = sum(z[k, :] @ R @ z[k, :] for k in range(N))
obj = obj1 + obj2

m.setObjective(obj, GRB.MINIMIZE)

# Save the model
m.write("mpc.lp")

# Run MPC
m.reset(0) # Clear previous results
m.params.NonConvex = 2 # To allow division operator
m.optimize()

# Obtain the results of the optimization
names_to_retrieve = ["u_41", "u_43"]

# Only get values of u, x, and C
for i in range(N):
    for j in range(4):
        names_to_retrieve.append(f"u[{i},{j}]")
        names_to_retrieve.append(f"x[{i},{j}]")

if m.Status == GRB.INFEASIBLE:
    print("Model is infeasible!")
    m.computeIIS() # Check for constraints leading to infeasibility
else:
    for v in m.getVars():
        if v.VarName in names_to_retrieve:
            print('%s %g' % (v.VarName, v.X))