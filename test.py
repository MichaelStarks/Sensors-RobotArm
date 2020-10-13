import numpy as np
#
# # Length of links in cm
# a1= 14.44625
# a2 = 14.44625
# a3 = 13.97
#
# # Desired Position of End effector
# px = 10 * 2.54
# py = 4 * 2.54
#
# phi = 140
# phi = deg2rad(phi)
#
# # Equations for Inverse kinematics
# wx = px - a3*cos(phi)
# wy = py - a3*sin(phi)
#
# delta = wx**2 + wy**2
# c2 = ( delta -a1**2 -a2**2)/(2*a1*a2)
# s2 = sqrt(1-c2**2)  # elbow down
# theta_2 = arctan2(s2, c2)
#
# s1 = ((a1+a2*c2)*wy - a2*s2*wx)/delta
# c1 = ((a1+a2*c2)*wx + a2*s2*wy)/delta
# theta_1 = arctan2(s1,c1)
# theta_3 = phi-theta_1-theta_2
#
# print('theta_1: ', rad2deg(theta_1))
# print('theta_2: ', rad2deg(theta_2))
# print('theta_3: ', rad2deg(theta_3))


x = 4
y = 2
z = 1

BASE_HEIGHT = 0
UPPER_ARM = 5.6929134
FOREARM = 5.6889764
WRIST = 5.4015748

b = np.sqrt(x**2 + (z + WRIST)**2)
print(b)
c = np.sqrt(x**2 + z**2)
print(c)
num = (FOREARM**2 - UPPER_ARM**2-b**2)
print(num)
denom = (-2*UPPER_ARM*b)
print(denom)
alpha = np.arccos(num/denom)
print(alpha)
