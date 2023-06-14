import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
import numpy as np

def get_x_y_var(x_axis, y_axis):
    if x_axis == "Prediction Horizon (N)":
        x_var = [3,
                 4,
                 5,
                 6,
                 7,
                 8,
                 9,
                 10,
                 11,
                 12,
                 13,
                 14,
                 15,]
    elif x_axis == "Minimum Green Time (s)":
        x_var = [10,
                 12,
                 14,
                 16,
                 18,
                 20,
                 22,
                 24,
                 26,
                 28]
    elif x_axis == "Cycle Time (s)":
        x_var = [70,
                 80,
                 90,
                 100,
                 110,
                 120,
                 130,
                 140,
                 150,
                 160,
                 170,
                 180,
                 190,
                 200,]
    elif x_axis == "15-Minute Intervals":
        x_var = ["6:15",
                "6:30",
                "6:45",
                "7:00",
                "7:15",
                "7:30",
                "7:45",
                "8:00",
                "8:15",
                "8:30",
                "8:45",
                "9:00",
                "9:15",
                "9:30",
                "9:45",
                "10:00",
                "10:15",
                "10:30",
                "10:45",
                "11:00",
                "11:15",
                "11:30",
                "11:45",
                "12:00",
                "12:15",
                "12:30",
                "12:45",
                "13:00",
                "13:15",
                "13:30",
                "13:45",
                "14:00",
                "14:15",
                "14:30",
                "14:45",
                "15:00",
                "15:15",
                "15:30",
                "15:45",
                "16:00",
                "16:15",
                "16:30",
                "16:45",
                "17:00",
                "17:15",
                "17:30",
                "17:45",
                "18:00",
                "18:15",
                "18:30",
                "18:45",
                "19:00",
                "19:15",
                "19:30",
                "19:45",
                "20:00"]
    if y_axis == "Queue Time (%)":
        if x_axis == "Prediction Horizon (N)":
            y_var = [25.96,
                    24.52,
                    24.46,
                    26.42,
                    28.39,
                    29.65,
                    30.08,
                    31.17,
                    30.47,
                    30.60,
                    30.75,
                    30.73,
                    30.88]
        elif x_axis == "Minimum Green Time (s)":
            y_var = [30.55,
                    30.99,
                    30.91,
                    30.80,
                    29.55,
                    29.32,
                    28.49,
                    27.64,
                    24.48,
                    23.37]
        elif x_axis == "Cycle Time (s)":
            y_var = [41.81,
                    40.75,
                    35.78,
                    30.59,
                    27.35,
                    22.16,
                    17.32,
                    15.00,
                    13.08,
                    10.31,
                    8.18,
                    6.32,
                    5.10,
                    3.36]
    elif y_axis == "Queue Length (%)":
        if x_axis == "Prediction Horizon (N)":
            y_var = [38.00,
                    38.07,
                    37.85,
                    39.83,
                    41.02,
                    42.19,
                    43.31,
                    44.21,
                    43.81,
                    43.13,
                    44.12,
                    43.51,
                    43.51]
        elif x_axis == "Minimum Green Time (s)":
            y_var = [42.71,
                    43.25,
                    42.80,
                    42.51,
                    42.66,
                    42.45,
                    43.89,
                    43.41,
                    40.43,
                    40.39]
        elif x_axis == "Cycle Time (s)":
            y_var = [62.67,
                    55.22,
                    49.08,
                    43.54,
                    38.07,
                    30.22,
                    23.24,
                    15.97,
                    10.71,
                    4.16,
                    -2.13,
                    -9.89,
                    -14.05,
                    -22.27]
    elif y_axis == "Flow Rate (%)":
        if x_axis == "Prediction Horizon (N)":
            y_var = [0.46,
                    0.59,
                    0.70,
                    0.58,
                    0.58,
                    0.57,
                    0.64,
                    0.67,
                    0.66,
                    0.62,
                    0.66,
                    0.66,
                    0.64]
        elif x_axis == "Minimum Green Time (s)":
            y_var = [0.79,
                    0.69,
                    0.59,
                    0.54,
                    0.51,
                    0.32,
                    0.08,
                    -0.17,
                    -0.62,
                    -1.50]
        elif x_axis == "Cycle Time (s)":
            y_var = [-0.59,
                    0.01,
                    0.36,
                    0.71,
                    0.80,
                    0.89,
                    1.05,
                    0.94,
                    1.03,
                    1.10,
                    1.09,
                    1.14,
                    1.21,
                    1.22]
    elif y_axis == "MPC Queue Length (m)":
        y_var = [7.601712963,
                7.778912037,
                7.824268519,
                7.959912037,
                8.544541667,
                8.651759259,
                8.580231481,
                8.611976852,
                9.660930556,
                10.077375,
                10.48737037,
                9.964375,
                9.438736111,
                6.978972222,
                6.647375,
                4.941425926,
                4.788407407,
                4.650143519,
                4.694199074,
                4.510467593,
                5.169319444,
                4.605064815,
                4.925912037,
                4.650537037,
                4.776976852,
                4.084694444,
                4.163986111,
                5.016787037,
                9.158416667,
                12.05685185,
                10.50428704,
                11.59505556,
                13.01276852,
                16.83818519,
                15.16210648,
                16.30416204,
                20.44071296,
                23.87152778,
                19.32769907,
                19.02795833,
                20.52181481,
                25.36472685,
                23.29748611,
                20.26170833,
                16.75472222,
                17.92377315,
                18.431375,
                17.79721759,
                18.7566713,
                20.22661574,
                18.73301389,
                19.64527315,
                17.1532037,
                17.03355556,
                18.44643519,
                17.79590278]
    elif y_axis == "Fixed-Time Queue Length (m)":
        y_var = [11.12953241,
                12.43874537,
                13.10251389,
                13.68010185,
                20.52181481,
                23.94124537,
                24.76022222,
                27.48503241,
                26.85056019,
                27.48191667,
                23.61685648,
                20.91602315,
                21.78814815,
                17.91654167,
                17.66428704,
                19.18167593,
                19.53965278,
                19.04919907,
                18.49926389,
                19.10503241,
                18.97058796,
                18.8132963,
                18.9808287,
                18.71263889,
                18.36632407,
                17.7865,
                18.07484259,
                18.27921759,
                28.52334722,
                30.88586574,
                32.12926389,
                31.23539815,
                33.72039815,
                26.27224074,
                27.90881481,
                28.847125,
                34.20954167,
                36.07200463,
                33.6245,
                37.74968519,
                34.34569907,
                34.14343981,
                34.65464352,
                31.55450926,
                41.77741204,
                50.90643056,
                53.73936574,
                53.57815278,
                47.45199537,
                45.46719444,
                40.97197685,
                41.70346759,
                41.68305556,
                42.20420833,
                43.5639213,
                44.30925926]
    elif y_axis == "MPC Queue Time (s)":
        y_var = [15.05758684,
                17.16380394,
                17.08160299,
                17.16827731,
                15.88609966,
                16.47884687,
                16.57275772,
                16.01023891,
                16.0865113,
                16.00884802,
                16.38646669,
                16.85706788,
                22.71827614,
                16.48626254,
                15.08655126,
                11.37460317,
                11.25661376,
                11.19419862,
                11.27843137,
                11.00296589,
                12.42560463,
                11.60558839,
                11.82075976,
                11.62061522,
                11.77677625,
                10.70851293,
                10.92427497,
                12.66131665,
                16.56541648,
                16.42767159,
                17.56260908,
                17.65954664,
                21.41881275,
                26.62835165,
                27.55452946,
                27.93195786,
                27.3538874,
                28.12102874,
                26.29009077,
                26.65473925,
                27.39225902,
                28.64944853,
                28.23588342,
                28.29944547,
                25.75,
                26.57729314,
                26.01028481,
                26.21912988,
                25.8940678,
                27.03465003,
                26.96793308,
                26.88855634,
                27.88957768,
                27.83638535,
                28.55903328,
                27.60636615]
    elif y_axis == "Fixed-Time Queue Time (s)":
        y_var = [21.00660893,
                23.29528222,
                23.82029289,
                24.85431579,
                30.26768607,
                35.34644397,
                35.14101203,
                36.3766211,
                37.00983098,
                38.24309392,
                36.93522688,
                35.74649123,
                34.5364426,
                30.15975455,
                27.25240595,
                27.95884956,
                29.36414566,
                29.6342155,
                29.39259087,
                28.85761747,
                28.95943255,
                28.31893004,
                29.16050334,
                29.67287785,
                30.04712175,
                29.31099127,
                28.94279877,
                29.33854167,
                32.5342437,
                33.73007927,
                34.14866555,
                37.4273183,
                34.10998343,
                33.09326425,
                34.2059333,
                35.74945581,
                34.19977212,
                35.10015232,
                33.20897774,
                35.23729135,
                35.84196597,
                36.32644941,
                35.5724255,
                33.97345468,
                38.44985299,
                41.33736089,
                41.49106863,
                41.91477631,
                43.52995624,
                42.55822391,
                40.32512998,
                40.00311203,
                41.02436323,
                40.4123751,
                41.19766104,
                42.16653816]
    elif y_axis == "MPC Flow Rate (veh/hr)":
        y_var = [8752,
                8532,
                8656,
                8504,
                9716,
                9560,
                9656,
                9468,
                10260,
                9988,
                9744,
                9672,
                8308,
                8216,
                8264,
                8160,
                7776,
                7588,
                7648,
                7556,
                7128,
                6948,
                6996,
                6880,
                7088,
                6920,
                6972,
                6860,
                8660,
                8220,
                8220,
                8208,
                8152,
                7908,
                7952,
                7896,
                9192,
                8964,
                8968,
                8952,
                9204,
                9012,
                8964,
                8924,
                10516,
                10300,
                10264,
                10124,
                9436,
                9356,
                9448,
                9460,
                8372,
                8384,
                8452,
                8420]
    elif y_axis == "Fixed-Time Flow Rate (veh/hr)":
        y_var = [8776,
                8624,
                8700,
                8612,
                10068,
                9860,
                9844,
                9600,
                9724,
                9588,
                9680,
                9548,
                8916,
                8188,
                8264,
                8072,
                7696,
                7612,
                7672,
                7536,
                7104,
                6916,
                6964,
                6968,
                7096,
                6956,
                6948,
                6824,
                8732,
                8236,
                8276,
                8164,
                8144,
                7848,
                7972,
                7888,
                9276,
                9068,
                9152,
                8992,
                9064,
                9076,
                9208,
                9088,
                10756,
                10212,
                10004,
                9972,
                9260,
                9168,
                9180,
                9088,
                8312,
                8196,
                8324,
                8324]
    return x_var, y_var

def main():

    x_axis = "Minimum Green Time (s)"
    #x_axis = "Cycle Time (s)"
    #x_axis = "Prediction Horizon (N)"
    #y_axis = "Flow Rate (%)"
    #y_axis = "Queue Length (%)"
    y_axis = "Queue Time (%)"
    spread = 5

    #x_axis = "15-Minute Intervals"
    #y_axis = "MPC Queue Length (m)"
    #y_axis_2 = "Fixed-Time Queue Length (m)"
    #label = "Queue Length (m)"
    #y_axis = "MPC Queue Time (s)"
    #y_axis_2 = "Fixed-Time Queue Time (s)"
    #label = "Queue Time (s)"
    #y_axis = "MPC Flow Rate (veh/hr)"
    #y_axis_2 = "Fixed-Time Flow Rate (veh/hr)"
    #label = "Flow Rate (veh/hr)"
    #spread = 10

    x_var, y_var = get_x_y_var(x_axis, y_axis)

    # Broken Axis Plot
    '''
    plt.figure(1)
    bax = brokenaxes(ylims=((0,5),(35,65)))
    bax.plot(x_var, y_var, marker=".")
    bax.set_title(f"Average {y_axis} Improvement vs. {x_axis}")
    bax.set_xlabel(f"{x_axis}")
    bax.set_ylabel(f"Performance Improvement Average {y_axis}")
    # plt.legend()
    '''
    
    # Standard Plot
    '''
    plt.figure(figsize=(7, 6))
    plt.xticks(x_var[0::1],rotation=45)
    plt.plot(x_var, y_var, marker='.')
    plt.title(f"Average {y_axis} Improvement vs. {x_axis}", fontsize=14)
    plt.xlabel(f"{x_axis}", fontsize=13)
    plt.ylabel(f"Performance Improvement Average {y_axis}", fontsize=12)
    plt.ylim(round(min(y_var)-spread), round(max(y_var)+spread))
    plt.axhline(y = 0, color = 'r', linestyle = '--')
    plt.show()
    '''
    # Two variable plot:
    '''
    plt.figure(1, figsize=(7, 7))
    #plt.xticks(x_var[3::4], rotation=45)
    plt.plot(x_var, y_var, marker='.', label=y_axis)
    x_var, y_var_2 = get_x_y_var(x_axis, y_axis_2)
    plt.plot(x_var, y_var_2, marker='.', label=y_axis_2)
    plt.title(f"Average Queue Length in the Katipunan Ave. - Aurora Blvd. Intersection", fontsize=13)
    #plt.xlim((500,51000))
    plt.xticks(x_var[3::4], rotation=45)
    plt.xlabel(f"Time (s)", fontsize=13)
    plt.ylabel(f"{label}", fontsize=13)
    plt.legend()
    #plt.ylim()
    plt.axhline(y = 0, color = 'r', linestyle = '--')
    plt.show()
    '''
    # Pie chart plotting of demand
    '''
    # plt.gcf().autofmt_xdate()
    labels = ["Katipunan Ave. South", "Katipunan Ave. North", "Aurora Blvd. West", "Aurora Blvd. East (Westbound)", "Aurora Blvd. East (Southbound)"]
    sizes = [14.22, 17.55,	14.50, 51.40, 2.33] # morning rush hour
    #sizes = [17.56, 27.25, 21.00, 29.45, 4.74] # non rush hour
    #sizes = [12.46, 26.70, 30.47, 25.18, 5.20] # evening rush hour
    colors = ["c", "b", "tab:orange", "m", "g"]

    fig, ax = plt.subplots(1, figsize=(17, 8))
    #plt.figure(1, figsize=(14, 7))
    ax.pie(sizes, colors=colors, autopct='%1.1f%%', textprops={'fontsize': 24})
    plt.title("Demand Composition of Incoming Roads from 8:00 AM to 9:00 AM", fontsize=20)
    #plt.title("Demand Composition of Incoming Roads from 10:00 AM to 11:00 AM", fontsize=20)
    #plt.title("Demand Composition of Incoming Roads from 5:00 PM to 6:00 PM", fontsize=20)

    ax.legend(labels,
            loc="lower center",
            prop={'size': 14},
            bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.show()
    '''

    # Plot MPC-based TSC for varying vehicle count error
    mpc_ql_error = [29.49078067, 31.41526384, 31.52831467, 31.64088214, 31.77035617]
    mpc_qt_error = [25.88264626, 26.09637689, 26.14654485, 26.18363233, 26.20754507]
    mpc_flow_error = [2157.6250000, 2129.7321429, 2129.9285714, 2128.9107143, 2129.3178571]

    cycle_times = ["No Error", "2% Error", "5% Error", "10% Error", "20% Error"]
    #cycle_times = [15, 40, 65, 90, 115]
    #width = 10

    plt.figure()

    # Width of a bar 
    cycle_times = np.array(cycle_times)

    #plt.bar(cycle_times, fixed_time_perf_qt, width, label="Fixed-time TSC")
    plt.bar(cycle_times, mpc_ql_error, color="r", label="MPC-based TSC", width=0.5)
    #plt.bar(cycle_times+width, mpc_based_perf_qt, width, color="tab:orange", label="MPC-based TSC")
    plt.title("Average Queue Length of MPC-based TSC for Varying Vehicle Count Error")
    plt.title("Average Queue Time of MPC-based TSC for Varying Vehicle Count Error")
    plt.title("Average Flow Rate of MPC-based TSC for Varying Vehicle Count Error")
    plt.xlabel("Error (%)", fontsize=11)
    plt.ylabel("Average Queue Length (m)", fontsize=11)
    plt.ylabel("Average Queue Time (s)", fontsize=11)
    plt.ylabel("Average Flow Rate (veh/hr)", fontsize=11)
    #plt.xlim((65,163))
    #plt.xlim((0,109.5))
    plt.ylim((0,max(mpc_ql_error)*1.15))
    #plt.xticks([70,80,90,100,154], rotation=0)
    # First argument - A list of positions at which ticks should be placed
    # Second argument -  A list of labels to place at the given locations
    #plt.xticks(cycle_times, ("No Error", "2% Error", "5% Error", "10% Error", "20% Error"))
    #plt.legend()
    #plt.legend(loc='best')
    plt.gcf().autofmt_xdate()

    plt.show()

if __name__ == "__main__":
    main()
