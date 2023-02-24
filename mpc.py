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
import decimal

def uniformify(T, n):

  # Get uniform distribution of hourly traffic volume with 3600/T samples
  t = int(3600/T)
  p = np.empty(t)
  for i in range(len(p)):
    p[i] = int(n/t+0.5)
  sum_array = int(sum(p))

  # Ensure that sum is equal to n
  if sum_array != n:
    if sum_array > n:
      p[-1] = int(p[-1]-(sum_p-n))
    else:
      p[-1] = int(p[-1]+(n-sum_p))

  return p

def poissonify(T, n):

  # Get Poisson distribution of hourly traffic volume with 3600/T samples
  t = int(3600/T)
  p = np.random.poisson(n/t, t)
  sum_p = sum(p)

  # Scale entries and convert them into integers
  p = p*(n/sum(p))
  p = [int(round(p[i])) for i in range(len(p))]
  sum_p = int(sum(p))

  # Ensure that sum is equal to n
  if sum_p != n:
    if sum_p-n > n:
      p[-1] = int(p[-1]-(sum_p-n))
    else:
      p[-1] = int(p[-1]+(n-sum_p))
  
  return p

# Initialize a model
m = gp.Model("MPC")

# Prediction Horizon
N = 5 # (TUNABLE)

# Traffic model variables (s)
T = 200 # Control interval
L = 9  # Lost time (3 phases * 3s)

# Saturation flow rate (veh/hr -> veh/s)
S_1 = 3000*(1/3600) # Saturation flow (DUMMY)
S_2 = 3000*(1/3600) # Saturation flow (DUMMY)
S_3 = 3000*(1/3600) # Saturation flow (DUMMY)
S_4 = 3000*(1/3600) # Saturation flow (DUMMY)

# Demand values from 6 AM to 8 PM (veh/hr)
d_1 = np.array([1367.,1884.,1659.,1574.,1430.,1149.,1172.,886.,1074.,1451.,1292.,1432.,
                1082.,945.])
d_2 = np.array([2024.,2135.,1872.,2065.,2032.,1923.,1992.,1716.,1979.,2010.,2861.,2935.,
                2381.,2274.])
d_3 = np.array([1549.,1776.,1828.,1833.,1805.,1829.,1941.,1992.,2404.,2699.,2802.,3598.,
                3748.,3217.])
d_4 = np.array([4562.,4850.,5995.,3327.,2921.,2560.,2319.,4458.,3396.,3445.,3286.,3655.,
                3130.,2649.])

# Traffic model matrices

# # x is the state variable (vehicle count)
# # u is the control input (green time)
# # B contains the road link properties
# # D is the demand matrix

xmin = np.array([0,0,0,0])
#xmax = np.array([50,50,50,50]) # (TUNABLE)
xref = np.array([0,0,0,0]) # (TUNABLE)
umin = np.array([5,5,5,5]) # Cannot have a zero timer setting

xmin = np.tile(xmin, (N+1,1))
#xmax = np.tile(xmax, (N+1,1))
umin = np.tile(umin, (N,1))
#umax = np.tile(umax, (N,1))

x = m.addMVar(shape=(N+1,4), lb=xmin, vtype=GRB.INTEGER, name="x")
u = m.addMVar(shape=(N,4), lb=umin, vtype=GRB.INTEGER, name="u")

C = m.addVar(vtype=GRB.INTEGER, lb=20.0, name="C")
C_dummy = m.addVar(vtype=GRB.CONTINUOUS, name="C_dummy")

u_41 = m.addVar(vtype=GRB.INTEGER, lb=5.0, name="u_41")
u_43 = m.addVar(vtype=GRB.INTEGER, lb=5.0, name="u_43")

y = m.addMVar(shape=(N+1,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="y") # x(k_o+k)-x(k_o)
z = m.addMVar(shape=(N,4), lb=-GRB.INFINITY, vtype=GRB.CONTINUOUS, name="z") # u(k_o+k)-u(k_o)

B = np.array([[S_1,0,0,0],
              [0,S_2,0,0],
              [0,0,S_3,0],
              [0,0,0,S_4]
              ])
B = -T*B

d_1p = poissonify(T,d_1[0])
d_2p = poissonify(T,d_2[0])
d_3p = poissonify(T,d_3[0])
d_4p = poissonify(T,d_4[0])

d = np.array([[d_1p[0], d_2p[0], d_3p[0], d_4p[0]]])
for i in range(1,N):
  d = np.concatenate((d, [[d_1p[i], d_2p[i], d_3p[i], d_4p[i]]]))
D = d

#D = np.tile(d, (N,1))
#D = T*D

# Weighting matrices (1/xmax^2)
w_1 = 1/((960+287)**2)
w_2 = 1/((2661+184)**2)
w_3 = 1/((3312+436)**2)
w_4 = 1/((1083+3209+166)**2)
Q = np.array([[w_1,0,0,0],
              [0,w_2,0,0],
              [0,0,w_3,0],
              [0,0,0,w_4]
              ])

r_1 = 0.05 # (TUNABLE)
r_2 = 0.05 # (TUNABLE)
r_3 = 0.05 # (TUNABLE)
r_4 = 0.05 # (TUNABLE)
R = np.array([[r_1,0,0,0],
              [0,r_2,0,0],
              [0,0,r_3,0],
              [0,0,0,r_4]
              ])

# Constraints
m.addConstr(x[0, :] == np.array([0,0,0,0])) # Initial number of vehicles
for k in range(N):

  # Traffic model
  m.addConstr(x[k+1, :] == x[k, :] + u[k, :] @ B*C_dummy + D[k, :]) # (Bu(k))^T = u(k)^T B^T

  # Sum of green times and lost time must be equal to cycle time C
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
# Note: Transposition is handled by GUROBI
obj1 = sum(y[k, :] @ Q @ y[k, :] for k in range(N+1))
obj2 = sum(z[k, :] @ R @ z[k, :] for k in range(N))

obj = obj1 + obj2

# Set objective function
m.setObjective(obj, GRB.MINIMIZE)

# Check for infeasibility / unboundedness
m.setParam("DualReductions", 0) # Infeasible model check

# Run MPC
m.reset(0)
m.params.NonConvex = 2 # To allow division operator
m.setParam('TimeLimit', 30) # 30s time limit
#m.feasRelaxS(0, True, False, False)
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
      print('%s %g' % (v.VarName, v.X))
      if v.VarName[:3] == "u[0" or (v.VarName == "u_41" or v.VarName == "u_43"):
        u_res.append(v.X)

  # Post-processing of data
  for i in range(len(u_res)):
    if u_res[i] < 0:
      print(f"Negative green time detected!")
      break
    u_res[i] = int(u_res[i]+0.5) # Convert to integer

  vals['C'] = int(vals['C']+0.5) # Convert to integer

  print(f"u[0,:] = {u_res}")
  print(f"C = {vals['C']}")

#print(f"xmin = {xmin}")
#print(f"xmax = {xmax}")
#print(f"umin = {umin}")
#print(f"umax = {umax}")
#print(f"B = {B}")
#print(f"D = {D}")
#print(f"Q = {Q}")
#print(f"R = {R}")
