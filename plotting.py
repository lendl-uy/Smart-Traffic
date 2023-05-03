import matplotlib.pyplot as plt
import numpy as np

# TRENDS IN MINIMUM GREEN TIME

avg_ql = np.array([6.83, 7.51, 3.85, 7.29, -0.88, 0.30, 0.31, 0.35, 2.79, -3.07, -2.53])

avg_qt = np.array([-5.19, 15.06, 16.23, 12.36, 10.58, 14.01, 2.08, 6.56, 14.59, 15.19, 14.77])

avg_flow = np.array([1.27, 1.24, 1.29, 1.19, 1.01, 1.02, 0.84, 0.87, 0.89, 1.17, 1.28])

u_min = np.array([10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40])

plt.figure()
plt.plot(u_min, avg_ql, "b")
plt.title("Average Queue Length Improvement vs. Minimum Green Time")
plt.xlabel("Minimum Green Time (s)")
plt.ylabel("Performance Improvement of Average Queue Length (%)")
plt.axhline(0, color='black', linewidth=.5)
plt.xlim(10)
plt.ylim(-5, 10)
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(u_min, avg_qt, "b")
plt.title("Average Queue Time Improvement vs. Minimum Green Time")
plt.xlabel("Minimum Green Time (s)")
plt.ylabel("Performance Improvement of Average Queue Time (%)")
plt.axhline(0, color='black', linewidth=.5)
plt.xlim(10)
plt.ylim(-7, 20)
plt.legend()
plt.gcf().autofmt_xdate()

plt.figure()
plt.plot(u_min, avg_flow, "b")
plt.title("Average Flow Rate Improvement vs. Minimum Green Time")
plt.xlabel("Minimum Green Time (s)")
plt.ylabel("Performance Improvement of Average Flow Rate (%)")
plt.xlim(10)
plt.ylim(0, 4)
plt.legend()
plt.gcf().autofmt_xdate()

plt.show()