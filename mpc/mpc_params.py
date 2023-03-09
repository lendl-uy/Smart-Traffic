# Author: Jan Lendl R. Uy
# CoE 199 MPC Parameters

import numpy as np
import traffic_distribution as td

# Prediction Horizon
N = 12 # (TUNABLE)

# Traffic model variables (s)
T = 300 # Control interval (must be divisible to 3600)
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

# Consequence of road links unaffected by traffic signals (veh/hr)
d_1_out = np.array([628.+155.,755.+340.,464.+261.,429.+334.,418.+232.,421.+265.,
                    376.+308.,212.+184.,292.+188.,204.+287.,332.+380.,297.+534.,
                    304.+450.,209.+448.])
d_2_out = np.array([237.+126.,232.+150.,217.+131.,199.+156.,215.+159.,117.+116.,
                    57.+140.,230.+104.,217.+121.,170.+111.,169.+93.,184.+90.,
                    137.+86.,119.+74.])
d_3_out = np.array([302.,286.,355.,314.,332.,275.,262.,404.,445.,384.,517.,448.,
                    436.,365.])
d_4_out = np.array([124.,144.,162.,177.,298.,160.,217.,166.,216.,189.,165.,201.,
                    149.,124.])

# Traffic model matrices

# x is the state variable (vehicle count)
# u is the control input (green time)
xmin = np.array([0,0,0,0])
#xmax = np.array([50,50,50,50]) # (TUNABLE)
xref = np.array([0,0,0,0]) # (TUNABLE)
umin = np.array([5,5,5,5]) # Cannot have a zero timer setting

xmin = np.tile(xmin, (N+1,1))
#xmax = np.tile(xmax, (N+1,1))
umin = np.tile(umin, (N,1))
#umax = np.tile(umax, (N,1))

# B contains the road link properties
B = np.array([[S_1,0,0,0],
              [0,S_2,0,0],
              [0,0,S_3,0],
              [0,0,0,S_4]
              ])
B = -T*B

# D is the demand matrix
d_1p = td.poissonify(T,d_1[0]-d_1_out[0])
d_2p = td.poissonify(T,d_2[0]-d_2_out[0])
d_3p = td.poissonify(T,d_3[0]-d_3_out[0])
d_4p = td.poissonify(T,d_4[0]-d_4_out[0])
#print(f"d_1p = {d_1p}")
for i in range(1,len(d_1)):
  d_1p = np.append(d_1p, td.poissonify(T,d_1[i]-d_1_out[i]))
  d_2p = np.append(d_2p, td.poissonify(T,d_2[i]-d_2_out[i]))
  d_3p = np.append(d_3p, td.poissonify(T,d_3[i]-d_3_out[i]))
  d_4p = np.append(d_4p, td.poissonify(T,d_4[i]-d_4_out[i]))

d = np.array([[d_1p[0], d_2p[0], d_3p[0], d_4p[0]]])
for i in range(1,N):
  d = np.concatenate((d, [[d_1p[i], d_2p[i], d_3p[i], d_4p[i]]]))
D = d
#print(f"d_2p = {d_2p}")
#print(f"d_2p = {sum(d_2p)}")
#D = np.tile(d, (N,1))
#D = T*D

# Weighting matrix W (traffic volume penalization)
#w_1 = 1/((960+287)**2)
#w_2 = 1/((2661+184)**2)
#w_3 = 1/((3312+436)**2)
#w_4 = 1/((1083+3209+166)**2)
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
r_2 = 0.05 # (TUNABLE)
r_3 = 0.05 # (TUNABLE)
r_4 = 0.05 # (TUNABLE)
R = np.array([[r_1,0,0,0],
              [0,r_2,0,0],
              [0,0,r_3,0],
              [0,0,0,r_4]
              ])
