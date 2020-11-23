import numpy as np


BASE_HEIGHT = 4.07
UPPER_ARM = 5.7165354
FOREARM = 5.7165354
WRIST = 6.10236

phi = 380

# def disp(x,z):
    # a = np.sqrt(BASE_HEIGHT**2 + x**2)
    # alpha = np.tan(x/BASE_HEIGHT)
    # # print(alpha)
    # b = np.sqrt((z**2 + a**2) - (2.0 * z * a * np.cos(alpha)))
    # c = np.sqrt(x**2 + (WRIST+(z-BASE_HEIGHT))**2)
    # omega = np.arccos((c**2 + x** 2 - (WRIST + (z-BASE_HEIGHT))**2)/(2.0*c*x))
    # theta_2 = np.arccos((UPPER_ARM**2 + FOREARM**2 - c**2)/(2.0*UPPER_ARM*FOREARM))
    # epsilon = np.arccos((c**2+UPPER_ARM**2-FOREARM**2)/(2.0*c*UPPER_ARM))
    # theta_1 = np.pi - (epsilon + omega)
    # # print(np.degrees(epsilon + omega))
    # theta_1 = 59.0 + np.degrees(theta_1) - 20
    # theta_2 = 60.0 + np.degrees(theta_2) - 26
    # theta_3 = 54 + phi - theta_1 - theta_2
    # print("Shoulder: " + str(theta_1))
    # print("Elbow: " + str(theta_2))
    # # print("Wrist: " + str(theta_3))


def disp(x,z):
    a = np.sqrt(x**2 + BASE_HEIGHT**2)
    alpha = np.tan(x/BASE_HEIGHT)
    omega = np.tan((WRIST + (z-BASE_HEIGHT))/x)
    l = np.sqrt(x**2 + (WRIST + (z-BASE_HEIGHT))**2)
    epsilon = np.arccos((UPPER_ARM**2 + l**2-FOREARM**2)/(2*UPPER_ARM*l))
    theta_1 = np.pi - (epsilon + omega)
    theta_2 = np.arccos((UPPER_ARM**2 + FOREARM**2 -  l**2)/(2 * UPPER_ARM * FOREARM))
    print("Shoulder: " + str(np.degrees(theta_1) + 59))
    print("Elbow: " + str(np.degrees(theta_2) + 60))
