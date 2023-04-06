# Author: Jan Lendl R. Uy
# CoE 199 MPC Parameters

import numpy as np
#import traffic_distribution as td

from create_demand_mpc import create_dua_demand

# Tunable parameters
N = 5 # (TUNABLE)
u_min_val = 15 # (TUNABLE)
C_min = 50 # (TUNABLE)
C_max = 78 # (TUNABLE)
#C = 154
print(f"N = {N}")
print(f"u_min_val = {u_min_val}")
print(f"C_min = {C_min}")
print(f"C_max = {C_max}")

# Traffic model variables (s)
T = C_max # Control interval (must divide 3600 w/out decimal)
L = 9  # Lost time (3 phases * 3s)

# Saturation flow rate (veh/hr -> veh/s)
S_1 = 841*(1/3600) # Saturation flow
S_2 = 1510*(1/3600) # Saturation flow
S_3 = 2017*(1/3600) # Saturation flow
S_4 = 3200*(1/3600) # Saturation flow

# Demand values from 6 AM to 8 PM (veh/hr)
d_1 = np.array([1147., 1636., 1465., 1408., 1277., 995., 1046., 
                831., 1014., 1397., 1200., 1343., 1004., 894.])
d_2 = np.array([1955., 2061., 1809., 2004., 1981., 1874., 1911., 
                1655., 1902., 1945., 2808., 2877., 2332., 2229.])
d_3 = np.array([1294., 1495., 1494., 1489., 1527., 1576., 1692., 
                1802., 2149., 2443., 2479., 3283., 3464., 2960.])
d_4 = np.array([4095., 4426., 5537., 2997., 2486., 2209., 1936., 
                4093., 3041., 3086., 2975., 3273., 2820., 2416.])

# Consequence of road links unaffected by traffic signals (veh/hr)
d_1_out = np.array([570., 851., 536., 598., 498., 533., 558., 
                    344., 422., 437., 621., 743., 678., 607.])
d_2_out = np.array([296., 309., 285., 297., 326., 185., 119., 
                    273., 261., 217., 209., 216., 174., 148.])
d_3_out = np.array([243., 243., 284., 259., 281., 228., 233., 
                    376., 409., 363., 468., 405., 398., 338.])
d_4_out = np.array([44., 48., 53., 54., 98., 32., 66., 40., 
                    68., 48., 62., 93., 68., 54.])

# Proportionality constants of Aurora East green times


# Traffic model matrices

# x is the state variable (vehicle count)
# u is the control input (green time)
xmin = np.array([0,0,0,0])
#xmax = np.array([50,50,50,50]) # (TUNABLE)
xref = np.array([0,0,0,0]) # (TUNABLE)
umin = np.array([u_min_val,u_min_val,u_min_val,u_min_val]) # Cannot have a zero timer setting

xmin = np.tile(xmin, (N+1,1))
#xmax = np.tile(xmax, (N+1,1))
umin = np.tile(umin, (N,1))
#umax = np.tile(umax, (N,1))

# B contains the road link properties
'''
B = np.array([[S_1/C,0,0,0],
              [0,S_2/C,0,0],
              [0,0,S_3/C,0],
              [0,0,0,S_4/C]
              ])
'''
B = np.array([[S_1,0,0,0],
              [0,S_2,0,0],
              [0,0,S_3,0],
              [0,0,0,S_4]
              ])
B = -T*B

# D is the demand matrix
# Demand based on DUArouter-generated flow definitions
try:
    d_1p, d_2p, d_3p, d_4p, d_4cons = create_dua_demand(T, 50400, "sumo\\micro\\003\\tripinfo_003.xml")
except:
    print(f"Error in creating dua demand!")

#D = np.tile(d, (N,1))
#D = T*D

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