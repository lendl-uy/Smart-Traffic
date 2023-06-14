import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/


x=["Katipunan Ave. North","Katipunan Ave. South","Aurora Blvd. East to West","Aurora Blvd. East to South","Aurora Blvd. West"]
x.reverse()

#AM rush hour Green times
a=33 #Kn
b=a #ks
c=22 #Aw
d=11 #Ae2Ks
e=36 #Ae

r1=np.flip(np.array([0, 0, a+3,a+3,a+d+3+3]))#upfront red time
g= np.flip(np.array([a, b,e,d,c]))#green time
y= np.flip(np.array([3,3,3,3,3]))#3s yellow time
r2= np.flip(np.array([e+3, e+3, 0,c+3,0]))#rear red time

fig, ax = plt.subplots()

plt.barh(x, r1, color='red')
plt.barh(x, g, left=r1, color='lime')
plt.barh(x, y, left=r1+g, color='yellow')
plt.barh(x, r2, left=r1+g+y, color='red')
plt.xlabel("Time (s)")
plt.ylabel("Specific Road")

#plt.title("Green Time Distribution of Green Times for an Afternoon Rush Hour Window (5PM-6PM)")
#plt.title("Green Time Distribution of Green Times for a Morning Rush Hour Window (7AM-8AM)")
plt.title("Green Time Distribution of Green Times for a Non-Rush Hour Window (11AM-12PM)")

plt.show()
