# Author: Jan Lendl R. Uy
# CoE 199 MPC Parameters

import numpy as np
#import traffic_distribution as td

# Tunable parameters
N = 15 # (TUNABLE)
u_min_val = 11 # (TUNABLE)
C = 75 # (TUNABLE)
#error = 0.5
print(f"N = {N}")
print(f"u_min_val = {u_min_val}")
print(f"C = {C}")

# Variable to store number of model relaxation
num_relaxation = 0

# Traffic model variables (s)
L = 9  # Lost time (3 phases * 3s)

# Saturation flow rate (veh/hr -> veh/s)
S_1 = 1189.79*(1/3600) # Saturation flow of Katipunan Ave South
S_2 = 2095.93*(1/3600) # Saturation flow of Katipunan Ave North
S_3 = 2081.93*(1/3600) # Saturation flow of Aurora Blvd West
S_4 = 3242.14*(1/3600) # Saturation flow of Aurora Blvd East to West
S_5 = 487.36*(1/3600) # Saturation flow of Aurora Blvd East to Katipunan South

# Demand values from 6 AM to 8 PM (veh/hr)
d_1 = np.array([1147., 1636., 1465., 1408., 1277., 995., 1046., 
                831., 1014., 1397., 1200., 1343., 1004., 894.])
d_2 = np.array([1955., 2061., 1809., 2004., 1981., 1874., 1911., 
                1655., 1902., 1945., 2808., 2877., 2332., 2229.])
d_3 = np.array([1294., 1495., 1494., 1489., 1527., 1576., 1692., 
                1802., 2149., 2443., 2479., 3283., 3464., 2960.])
d_43 = np.array([4095., 4426., 5537., 2997., 2486., 2209., 1936., 
                4093., 3041., 3086., 2975., 3273., 2820., 2416.])
d_41 = np.array([280., 275., 240., 184., 345., 261., 171., 1069., 
                  1128., 714., 671., 560., 421, 504.])

# Consequence of road links unaffected by traffic signals (veh/hr)
d_1_out = np.array([570., 851., 536., 598., 498., 533., 558., 
                    344., 422., 437., 621., 743., 678., 607.])
d_2_out = np.array([296., 309., 285., 297., 326., 185., 119., 
                    273., 261., 217., 209., 216., 174., 148.])
d_3_out = np.array([243., 243., 284., 259., 281., 228., 233., 
                    376., 409., 363., 468., 405., 398., 338.])
d_43_out = np.array([44., 48., 53., 54., 98., 32., 66., 40., 
                    68., 48., 62., 93., 68., 54.])

# Subtract inflow to outflow then convert to veh/s
d_1 = (d_1-d_1_out)*(1/3600)
d_2 = (d_2-d_2_out)*(1/3600)
d_3 = (d_3-d_3_out)*(1/3600)
d_43 = (d_43-d_43_out-d_41)*(1/3600)
d_41 = d_41*(1/3600)

# TRAFFIC MODEL MATRICES

# x is the state variable (vehicle count)
# u is the control input (green time)
xref = np.array([0,0,0,0,0])
xmin = xref
xmax = np.array([250,250,400,400,120]) # (TUNABLE)
umin = np.array([0,0,0,0,0]) # Cannot have a zero timer setting

xmin = np.tile(xmin, (N+1,1))
#xmax = np.tile(xmax, (N+1,1))
umin = np.tile(umin, (N,1))

# B contains the road link properties
'''
B = np.array([[S_1/C,0,0,0],
              [0,S_2/C,0,0],
              [0,0,S_3/C,0],
              [0,0,0,S_4/C]
              ])
'''
B = np.array([[S_1,0,0,0,0],
              [0,S_2,0,0,0],
              [0,0,S_3,0,0],
              [0,0,0,S_4,0],
              [0,0,0,0,S_5]
              ])
B = -1*B

# D is the demand matrix
# Demand based on DUArouter-generated flow definitions
'''
try:
    d_1p, d_2p, d_3p, d_4p, d_41p = create_dua_demand(T, 50400, "sumo\\micro\\003\\tripinfo_003.xml")
except:
    print(f"Error in creating dua demand!")
'''
#D = np.tile(d, (N,1))
#D = T*D

# Weighting matrix W (traffic volume penalization)
w_1 = 1/((960)**2)
w_2 = 1/((3312)**2)
w_3 = 1/((3312)**2)
w_4 = 1/((1137)**2)
w_5 = 1/((1000)**2)
Q = np.array([[w_1,0,0,0,0],
              [0,w_2,0,0,0],
              [0,0,w_3,0,0],
              [0,0,0,w_4,0],
              [0,0,0,0,w_5]
              ])

# Weighting matrix R (control input penalization)
r_1 = 0.05 # (TUNABLE)
r_2 = 0.25 # (TUNABLE)
r_3 = 0.05 # (TUNABLE)
r_4 = 0.25 # (TUNABLE)
r_5 = 0.1 # (TUNABLE)
R = np.array([[r_1,0,0,0,0],
              [0,r_2,0,0,0],
              [0,0,r_3,0,0],
              [0,0,0,r_4,0],
              [0,0,0,0,r_5]
              ])