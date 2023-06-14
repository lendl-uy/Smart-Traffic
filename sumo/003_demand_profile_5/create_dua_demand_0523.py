from bs4 import BeautifulSoup
import numpy as np

directory = "4-3-test-demand-vianetedit-ref.rou.xml"
filename = "4-3-test-demand-vianetedit.rou.xml"

# Katipunan South
katip_s_aurora_w_car = [354.00, 447.00, 525.00, 478.00, 441.00, 231.00, 255.00, 294.00, 322.00, 786.00, 338.00, 310.00, 157.00, 138.00]
katip_s_aurora_w_taxi = [25.00, 46.00, 42.00, 39.00, 27.00, 21.00, 18.00, 12.00, 22.00, 12.00, 18.00, 18.00, 10.00, 7.00]
katip_s_aurora_w_bus = [9.00, 2.00, 11.00, 11.00, 9.00, 7.00, 6.00, 8.00, 9.00, 9.00, 7.00, 6.00, 4.00, 2.00]
katip_s_aurora_w_truck = [5.00, 11.00, 10.00, 19.00, 21.00, 23.00, 18.00, 24.00, 37.00, 14.00, 28.00, 24.00, 6.00, 4.00]
katip_s_aurora_w_trailer = [0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 1.00, 1.00, 1.00, 1.00, 0.00, 0.00, 0.00]
katip_s_aurora_w_motorcycle = [184.00, 279.00, 341.00, 262.00, 281.00, 180.00, 191.00, 148.00, 201.00, 138.00, 187.00, 242.00, 149.00, 136.00]

katip_s_aurora_e_car = [60.00, 132.00, 106.00, 133.00, 88.00, 93.00, 152.00, 83.00, 87.00, 93.00, 120.00, 188.00, 156.00, 186.00]
katip_s_aurora_e_taxi = [2.00, 10.00, 9.00, 34.00, 13.00, 21.00, 11.00, 9.00, 7.00, 12.00, 15.00, 9.00, 7.00, 12.00]
katip_s_aurora_e_bus = [1.00, 2.00, 0.00, 2.00, 1.00, 0.00, 0.00, 0.00, 0.00, 2.00, 1.00, 0.00, 0.00, 3.00]
katip_s_aurora_e_truck = [6.00, 5.00, 3.00, 2.00, 0.00, 3.00, 1.00, 4.00, 5.00, 14.00, 4.00, 7.00, 5.00, 10.00]
katip_s_aurora_e_trailer = [0.00, 0.00, 0.00, 0.00, 0.00, 2.00, 0.00, 0.00, 2.00, 0.00, 2.00, 0.00, 0.00, 0.00]
katip_s_aurora_e_motorcycle = [56.00, 149.00, 99.00, 139.00, 106.00, 128.00, 137.00, 79.00, 80.00, 157.00, 229.00, 310.00, 269.00, 226.00]

katip_s_u_turn_car = [445.00, 553.00, 319.00, 288.00, 290.00, 286.00, 257.00, 169.00, 241.00, 159.00, 250.00, 229.00, 241.00, 170.00]
katip_s_u_turn_taxi = [18.00, 20.00, 6.00, 17.00, 6.00, 3.00, 2.00, 2.00, 10.00, 2.00, 9.00, 7.00, 10.00, 6.00]
katip_s_u_turn_bus = [1.00, 7.00, 4.00, 8.00, 2.00, 3.00, 2.00, 5.00, 4.00, 3.00, 6.00, 4.00, 5.00, 2.00]
katip_s_u_turn_truck = [1.00, 7.00, 5.00, 8.00, 15.00, 13.00, 11.00, 11.00, 3.00, 6.00, 2.00, 4.00, 5.00, 3.00]
katip_s_u_turn_trailer = [0.00, 1.00, 0.00, 0.00, 2.00, 0.00, 0.00, 1.00, 0.00, 0.00, 2.00, 0.00, 1.00, 1.00]
katip_s_u_turn_motorcycle = [143.00, 151.00, 114.00, 100.00, 94.00, 106.00, 97.00, 22.00, 30.00, 32.00, 56.00, 48.00, 38.00, 25.00]

# Katipunan North
katip_n_aurora_w_car = [64.00, 70.00, 78.00, 58.00, 44.00, 44.00, 16.00, 48.00, 56.00, 46.00, 50.00, 48.00, 22.00, 20.00]
katip_n_aurora_w_taxi = [42.00, 21.00, 20.00, 24.00, 21.00, 11.00, 7.00, 10.00, 11.00, 6.00, 16.00, 10.00, 31.00, 24.00]
katip_n_aurora_w_bus = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
katip_n_aurora_w_truck = [3.00, 0.00, 5.00, 4.00, 8.00, 6.00, 1.00, 2.00, 6.00, 5.00, 5.00, 2.00, 2.00, 1.00]
katip_n_aurora_w_trailer = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
katip_n_aurora_w_motorcycle = [121.00, 141.00, 104.00, 113.00, 141.00, 54.00, 31.00, 168.00, 141.00, 112.00, 97.00, 124.00, 82.00, 74.00]

katip_n_aurora_e_car = [554.00, 710.00, 642.00, 764.00, 710.00, 780.00, 870.00, 621.00, 763.00, 824.00, 1041.00, 745.00, 519.00, 698.00]
katip_n_aurora_e_taxi = [24.00, 39.00, 37.00, 52.00, 54.00, 67.00, 48.00, 52.00, 57.00, 53.00, 60.00, 43.00, 31.00, 42.00]
katip_n_aurora_e_bus = [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
katip_n_aurora_e_truck = [88.00, 76.00, 79.00, 104.00, 130.00, 116.00, 98.00, 118.00, 109.00, 102.00, 140.00, 55.00, 55.00, 77.00]
katip_n_aurora_e_trailer = [6.00, 3.00, 1.00, 5.00, 10.00, 8.00, 10.00, 7.00, 5.00, 10.00, 8.00, 3.00, 5.00, 4.00]
katip_n_aurora_e_motorcycle = [986.00, 924.00, 765.00, 782.00, 751.00, 718.00, 766.00, 584.00, 707.00, 739.00, 1350.00, 1815.00, 1548.00, 1260.00]

katip_n_u_turn_car = [66.00, 77.00, 78.00, 98.00, 112.00, 70.00, 63.00, 45.00, 47.00, 48.00, 41.00, 32.00, 37.00, 29.00]
katip_n_u_turn_taxi = [2.00, 4.00, 5.00, 1.00, 3.00, 1.00, 1.00, 1.00, 3.00, 2.00, 0.00, 1.00, 0.00, 0.00]
katip_n_u_turn_bus = [0.00, 2.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
katip_n_u_turn_truck = [2.00, 1.00, 0.00, 4.00, 1.00, 2.00, 4.00, 1.00, 1.00, 0.00, 1.00, 0.00, 1.00, 0.00]
katip_n_u_turn_trailer = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
katip_n_u_turn_motorcycle = [38.00, 30.00, 33.00, 32.00, 31.00, 27.00, 57.00, 39.00, 48.00, 41.00, 36.00, 38.00, 27.00, 25.00]

# Aurora West
aurora_w_aurora_e_car = [401.00, 552.00, 434.00, 461.00, 550.00, 628.00, 580.00, 628.00, 702.00, 874.00, 894.00, 959.00, 1005.00, 889.00]
aurora_w_aurora_e_taxi = [45.00, 42.00, 55.00, 86.00, 56.00, 73.00, 82.00, 60.00, 90.00, 97.00, 89.00, 96.00, 101.00, 91.00]
aurora_w_aurora_e_bus = [6.00, 8.00, 8.00, 13.00, 12.00, 5.00, 8.00, 5.00, 10.00, 7.00, 10.00, 9.00, 9.00, 5.00]
aurora_w_aurora_e_truck = [18.00, 20.00, 22.00, 30.00, 31.00, 35.00, 42.00, 25.00, 24.00, 51.00, 39.00, 31.00, 26.00, 16.00]
aurora_w_aurora_e_trailer = [0.00, 0.00, 2.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 3.00, 0.00, 0.00]
aurora_w_aurora_e_motorcycle = [581.00, 630.00, 689.00, 640.00, 597.00, 607.00, 747.00, 708.00, 914.00, 1051.00, 979.00, 1780.00, 1925.00, 1621.00]

aurora_w_katip_s_car = [121.00, 107.00, 115.00, 110.00, 104.00, 96.00, 89.00, 137.00, 199.00, 150.00, 184.00, 175.00, 167.00, 139.00]
aurora_w_katip_s_taxi = [13.00, 12.00, 13.00, 12.00, 7.00, 7.00, 20.00, 25.00, 24.00, 25.00, 23.00, 25.00, 20.00, 10.00]
aurora_w_katip_s_bus = [0.00, 3.00, 1.00, 0.00, 2.00, 2.00, 1.00, 2.00, 2.00, 2.00, 2.00, 2.00, 0.00, 1.00]
aurora_w_katip_s_truck = [0.00, 10.00, 8.00, 9.00, 22.00, 14.00, 7.00, 9.00, 5.00, 9.00, 8.00, 5.00, 6.00, 3.00]
aurora_w_katip_s_trailer = [0.00, 0.00, 0.00, 0.00, 2.00, 1.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
aurora_w_katip_s_motorcycle = [109.00, 111.00, 147.00, 128.00, 144.00, 108.00, 116.00, 202.00, 179.00, 177.00, 251.00, 198.00, 205.00, 185.00]

# Aurora East
aurora_e_katip_s_car = [123.00, 110.00, 98.00, 98.00, 152.00, 125.00, 81.00, 565.00, 540.00, 322.00, 299.00, 253.00, 194.00, 245.00]
aurora_e_katip_s_taxi = [13.00, 8.00, 7.00, 3.00, 12.00, 7.00, 6.00, 21.00, 15.00, 23.00, 18.00, 21.00, 13.00, 10.00]
aurora_e_katip_s_bus = [1.00, 1.00, 0.00, 1.00, 0.00, 0.00, 1.00, 0.00, 0.00, 1.00, 0.00, 3.00, 1.00, 2.00]
aurora_e_katip_s_truck = [9.00, 10.00, 7.00, 5.00, 2.00, 2.00, 3.00, 5.00, 5.00, 8.00, 6.00, 15.00, 9.00, 8.00]
aurora_e_katip_s_trailer = [1.00, 11.00, 2.00, 1.00, 0.00, 0.00, 1.00, 0.00, 0.00, 1.00, 0.00, 9.00, 7.00, 4.00]
aurora_e_katip_s_motorcycle = [133.00, 135.00, 126.00, 76.00, 179.00, 127.00, 79.00, 478.00, 568.00, 359.00, 348.00, 259.00, 197.00, 235.00]

aurora_e_katip_n_car = [44.00, 48.00, 53.00, 54.00, 98.00, 32.00, 66.00, 40.00, 68.00, 48.00, 62.00, 93.00, 68.00, 54.00]
aurora_e_katip_n_taxi = [0.00, 0.00, 7.00, 6.00, 8.00, 3.00, 3.00, 2.00, 2.00, 2.00, 4.00, 9.00, 4.00, 4.00]
aurora_e_katip_n_bus = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00]
aurora_e_katip_n_truck = [32.00, 51.00, 47.00, 60.00, 121.00, 94.00, 88.00, 67.00, 81.00, 72.00, 53.00, 37.00, 22.00, 25.00]
aurora_e_katip_n_trailer = [2.00, 2.00, 6.00, 5.00, 18.00, 7.00, 15.00, 6.00, 8.00, 11.00, 9.00, 4.00, 6.00, 4.00]
aurora_e_katip_n_motorcycle = [46.00, 43.00, 47.00, 51.00, 52.00, 24.00, 44.00, 48.00, 56.00, 56.00, 35.00, 55.00, 46.00, 35.00]

aurora_e_aurora_w_car = [1530.00, 890.00, 1647.00, 1284.00, 589.00, 741.00, 594.00, 1214.00, 799.00, 950.00, 849.00, 1059.00, 864.00, 688.00]
aurora_e_aurora_w_taxi = [104.00, 802.00, 165.00, 81.00, 111.00, 88.00, 48.00, 126.00, 101.00, 98.00, 90.00, 129.00, 75.00, 106.00]
aurora_e_aurora_w_bus = [10.00, 10.00, 18.00, 10.00, 8.00, 5.00, 1.00, 11.00, 7.00, 9.00, 12.00, 14.00, 9.00, 12.00]
aurora_e_aurora_w_truck = [23.00, 15.00, 49.00, 34.00, 69.00, 64.00, 31.00, 71.00, 51.00, 59.00, 42.00, 34.00, 21.00, 36.00]
aurora_e_aurora_w_trailer = [0.00, 1.00, 0.00, 1.00, 2.00, 3.00, 2.00, 1.00, 0.00, 1.00, 1.00, 2.00, 1.00, 1.00]
aurora_e_aurora_w_motorcycle = [2104.00, 2385.00, 3365.00, 1349.00, 1264.00, 1015.00, 1023.00, 1561.00, 887.00, 1207.00, 1248.00, 1382.00, 1361.00, 1015.00]

katip_s_aurora_w = [katip_s_aurora_w_car, katip_s_aurora_w_taxi, katip_s_aurora_w_bus, 
                    katip_s_aurora_w_truck, katip_s_aurora_w_trailer, katip_s_aurora_w_motorcycle]
katip_s_u_turn = [katip_s_u_turn_car, katip_s_aurora_e_taxi, katip_s_aurora_e_bus, 
                  katip_s_aurora_e_truck, katip_s_aurora_e_trailer, katip_s_aurora_e_motorcycle]
katip_n_u_turn = [katip_n_u_turn_car, katip_n_u_turn_taxi, katip_n_u_turn_bus, katip_n_u_turn_truck, 
                  katip_n_u_turn_trailer, katip_n_u_turn_motorcycle]
katip_s_aurora_e = [katip_s_aurora_e_car, katip_s_aurora_e_taxi, katip_s_aurora_e_bus, 
                    katip_s_aurora_e_truck, katip_s_aurora_e_trailer, katip_s_aurora_e_motorcycle]
aurora_e_katip_n = [aurora_e_katip_n_car, aurora_e_katip_n_taxi, aurora_e_katip_n_bus, aurora_e_katip_n_truck, 
                    aurora_e_katip_n_trailer, aurora_e_katip_n_motorcycle]
aurora_e_aurora_w = [aurora_e_aurora_w_car, aurora_e_aurora_w_taxi, aurora_e_aurora_w_bus, aurora_e_aurora_w_truck, 
                     aurora_e_aurora_w_trailer, aurora_e_aurora_w_motorcycle]
katip_n_aurora_w = [katip_n_aurora_w_car, katip_n_aurora_w_taxi, katip_n_aurora_w_bus, katip_n_aurora_w_truck, 
                    katip_n_aurora_w_trailer, katip_n_aurora_w_motorcycle]
katip_n_aurora_e = [katip_n_aurora_e_car, katip_n_aurora_e_taxi, katip_n_aurora_e_bus, katip_n_aurora_e_truck, 
                    katip_n_aurora_e_trailer, katip_n_aurora_e_motorcycle]
aurora_w_aurora_e = [aurora_w_aurora_e_car, aurora_w_aurora_e_taxi, aurora_w_aurora_e_bus, aurora_w_aurora_e_truck, 
                     aurora_w_aurora_e_trailer, aurora_w_aurora_e_motorcycle]
aurora_w_katip_s = [aurora_w_katip_s_car, aurora_w_katip_s_taxi, aurora_w_katip_s_bus, aurora_w_katip_s_truck, 
                    aurora_w_katip_s_trailer, aurora_w_katip_s_motorcycle]
aurora_e_katip_s = [aurora_e_katip_s_car, aurora_e_katip_s_taxi, aurora_e_katip_s_bus, aurora_e_katip_s_truck, 
                    aurora_e_katip_s_trailer, aurora_e_katip_s_motorcycle]

''' 
#DEMAND PROFILE 1 Aurora West compensates for halved Aurora east demand
aurora_w_demand = 1.778639311
aurora_e_demand = 0.5
katip_n_demand = 1.0
katip_s_demand = 1.0
'''
'''
#DEMAND PROFILE 2 From aurora west and east and added to katip south
aurora_w_demand = 0.75
aurora_e_demand = 0.75
katip_n_demand = 1.977382197
katip_s_demand = 1.0
'''
'''
#DEMAND PROFILE 3 Katip North and South demand goes to Aurora West
aurora_w_demand = 1.394551755
aurora_e_demand = 1.0
katip_n_demand = 0.75
katip_s_demand = 0.75
'''
'''
#DEMAND PROFILE 4
aurora_w_demand = 0.7413585258
aurora_e_demand = 0.6639127561
katip_n_demand = 1.369291589
katip_s_demand = 2.41207076
'''

#DEMAND PROFILE 5
aurora_w_demand = 0.5
aurora_e_demand = 0.5
katip_n_demand = 0.5
katip_s_demand = 0.5

katip_s_aurora_w_adjusted = np.round(katip_s_demand*np.array(katip_s_aurora_w, dtype=np.float32), 0)
katip_s_u_turn_adjusted = np.round(katip_s_demand*np.array(katip_s_u_turn, dtype=np.float32), 0)
katip_n_u_turn_adjusted = np.round(katip_n_demand*np.array(katip_n_u_turn, dtype=np.float32), 0)
katip_s_aurora_e_adjusted = np.round(katip_s_demand*np.array(katip_s_aurora_e, dtype=np.float32), 0)
aurora_e_katip_n_adjusted = np.round(aurora_e_demand*np.array(aurora_e_katip_n, dtype=np.float32), 0)
aurora_e_aurora_w_adjusted = np.round(aurora_e_demand*np.array(aurora_e_aurora_w, dtype=np.float32), 0)
katip_n_aurora_w_adjusted = np.round(katip_n_demand*np.array(katip_n_aurora_w, dtype=np.float32), 0)
katip_n_aurora_e_adjusted = np.round(katip_n_demand*np.array(katip_n_aurora_e, dtype=np.float32), 0)
aurora_w_aurora_e_adjusted = np.round(aurora_w_demand*np.array(aurora_w_aurora_e, dtype=np.float32), 0)
aurora_w_katip_s_adjusted = np.round(aurora_w_demand*np.array(aurora_w_katip_s, dtype=np.float32), 0)
aurora_e_katip_s_adjusted = np.round(aurora_e_demand*np.array(aurora_e_katip_s, dtype=np.float32), 0)

# For verification purposes
sum_katip_s_aurora_w_adjusted = np.sum(katip_s_aurora_w_adjusted, axis=0)
sum_katip_s_aurora_e_adjusted = np.sum(katip_s_aurora_e_adjusted, axis=0)
sum_katip_s_u_turn_adjusted = np.sum(katip_s_u_turn_adjusted, axis=0)

sum_katip_n_u_turn_adjusted = np.sum(katip_n_u_turn_adjusted, axis=0)
sum_katip_n_aurora_w_adjusted = np.sum(katip_n_aurora_w_adjusted, axis=0)
sum_katip_n_aurora_e_adjusted = np.sum(katip_n_aurora_e_adjusted, axis=0)

sum_aurora_w_aurora_e_adjusted = np.sum(aurora_w_aurora_e_adjusted, axis=0)
sum_aurora_w_katip_s_adjusted = np.sum(aurora_w_katip_s_adjusted, axis=0)

sum_aurora_e_katip_n_adjusted = np.sum(aurora_e_katip_n_adjusted, axis=0)
sum_aurora_e_aurora_w_adjusted = np.sum(aurora_e_aurora_w_adjusted, axis=0)
sum_aurora_e_katip_s_adjusted = np.sum(aurora_e_katip_s_adjusted, axis=0)

print(f"katip_s = {np.sum(sum_katip_s_aurora_w_adjusted+sum_katip_s_aurora_e_adjusted+sum_katip_s_u_turn_adjusted)}")
print(f"katip_n = {np.sum(sum_katip_n_u_turn_adjusted+sum_katip_n_aurora_w_adjusted+sum_katip_n_aurora_e_adjusted)}")
print(f"aurora_w = {np.sum(sum_aurora_w_aurora_e_adjusted+sum_aurora_w_katip_s_adjusted)}")
print(f"aurora_e = {np.sum(sum_aurora_e_katip_n_adjusted+sum_aurora_e_aurora_w_adjusted+sum_aurora_e_katip_s_adjusted)}")

'''
route_demand = [katip_s_aurora_w, katip_s_u_turn, katip_n_u_turn, katip_s_aurora_e,
                aurora_e_katip_n, aurora_e_aurora_w, katip_n_aurora_w, katip_n_aurora_e,
                aurora_w_aurora_e, aurora_w_katip_s, aurora_e_katip_s]
'''

route_demand = [katip_s_aurora_w_adjusted, katip_s_u_turn_adjusted, katip_n_u_turn_adjusted, katip_s_aurora_e_adjusted,
                aurora_e_katip_n_adjusted, aurora_e_aurora_w_adjusted, katip_n_aurora_w_adjusted, katip_n_aurora_e_adjusted,
                aurora_w_aurora_e_adjusted, aurora_w_katip_s_adjusted, aurora_e_katip_s_adjusted]

#print(f"route_demand = {route_demand}")

route_names = ["katip_s_aurora_w", "katip_s_u_turn", 
               "katip_n_u_turn", "katip_s_aurora_e", 
               "aurora_e_katip_n", "aurora_e_aurora_w", 
               "katip_n_aurora_w", "katip_n_aurora_e", 
               "aurora_w_aurora_e", "aurora_w_katip_s", 
               "aurora_e_katip_s"]

veh_types = ["CAR", "TAXI", "BUS", "TRUCK", "TRAILER", "MOTORCYCLE"]

# Reading data from the xml file
with open(directory, "r+") as f:
    data = f.read()

soup = BeautifulSoup(data, "xml")

#print(soup.prettify())

flows = soup.find_all("flow")

i = 0.00
j = 0.00

sim_time = 14

for l in range(sim_time):
  for m in range(11):
    for o in range(len(veh_types)):
      # Initialize attributes of new flow
      id_name = f"f_{m}_{l}_{veh_types[o]}"
      if m == 2:
        id_name = f"f_10_{l}_{veh_types[o]}"
      elif m > 2:
        id_name = f"f_{m-1}_{l}_{veh_types[o]}"

      if route_demand[m][o][l] == 0.00:
        #print(f"{id_name} has zero demand!")
        continue

      new_flow = soup.new_tag("flow")

      new_flow["id"] = id_name
      i = j
      new_flow["begin"] = str(i)
      new_flow["route"] = route_names[m]
      i += 3600.00
      new_flow["end"] = str(i)
      new_flow["type"] = veh_types[o]
      new_flow["vehsPerHour"] = route_demand[m][o][l]

      # Add new flow defintion to the XML file
      soup.routes.append(new_flow)
  j += 3600.00

#print(soup.prettify())

f = open(filename, "w")
f.write(soup.prettify())
f.close()