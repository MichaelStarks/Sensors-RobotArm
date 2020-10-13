import time
import math
import queue as Q
import threading
import numpy as np
from dynio import *


class RobotArm:

    def __init__(self):
        self.motors = [] # Motors are ordered from bottem to top
        self.home_angle = [] # Motors are ordered from bottem to top
        self.q = Q.LifoQueue()
        self.returns = Q.LifoQueue()
        self.robot_arm_dxl = None
        self.robot_arm_dxl = dxl.DynamixelIO("/dev/ttyUSB0")
        self.BASE_HEIGHT = 4.3897638
        self.UPPER_ARM = 5.6929134
        self.FOREARM = 5.6889764
        self.WRIST = 5.4015748
        for i in range(1,9):
            # print(i)
            self.motors.append(self.robot_arm_dxl.new_ax12(i))
            self.motors[-1].torque_enable()
            self.motors[-1].set_position_mode()
        # self.set_elbow(0)
        __start__ = threading.Thread(target=self.__start__,args=(),daemon=True)
        __start__.start()
        self.calibrate()
        self.q.put((self.motors[2].set_velocity_mode,[]))
        self.q.put((self.motors[4].set_velocity_mode,[]))
        __shoulder_thread__ = threading.Thread(target=self.__motor_assist_shoulder__, args=(),daemon=True)
        __shoulder_thread__.start()
        __elbow_thread__ = threading.Thread(target=self.__motor_assist_shoulder__, args=(),daemon=True)
        __elbow_thread__.start()

        # self.__denavit_hartenberg_maritx__()


    def __del__(self):
        self.home()

    def __start__(self):
        while True:
            items = self.q.get()
            # print(items)
            func = items[0]
            args = items[1]
            self.returns.put(func(*args))

    def __motor_assist_shoulder__(self):
        velocity = 1023
        current_shoulder = 0
        goal_shoulder = 0
        self.q.put((self.motors[1].get_position,[]))
        temp = self.returns.get()
        while temp is None:
            temp = self.returns.get()
        current_shoulder = temp
        self.q.put((self.motors[1].read_control_table,["Goal_Position"]))
        temp = self.returns.get()
        while temp is None:
            temp = self.returns.get()
        goal_shoulder = temp
        if goal_shoulder == current_shoulder:
            direction_shoulder = 0
        else:
            direction_shoulder = (goal_shoulder-current_shoulder)/abs(goal_shoulder-current_shoulder)
        print("test")
        self.q.put((self.motors[2].set_velocity,[direction_shoulder*velocity]))

    def __motor_assist_elbow__(self):
        velocity = 1023
        current_elbow = 0
        goal_elbow = 0
        self.q.put((self.motors[1].get_position(),[]))
        temp = self.returns.get()
        while temp is None:
            temp = self.returns.get()
        current_elbow = temp
        self.q.put((self.motors[3].read_control_table(),["Goal_Position"]))
        temp = self.returns.get()
        while temp is None:
            temp = self.returns.get()
        goal_elbow = temp
        if goal_elbow == current_elbow:
            direction_shoulder = 0
        else:
            direction_elbow = (goal_elbow-current_elbow)/abs(goal_elbow-current_elbow)
        self.q.put((self.motors[4].set_velocity,[direction_elbow*velocity]))

        # Calculates the Denavit-Hartenberg Maritx
    def __denavit_hartenberg_matrix__(self):
        # Matrix for the first frame (I can not explain the math you will have to go learn it)
        H0_1 = [[np.cos(np.radians(self.motors[1].get_angle())),-np.sin(np.radians(self.motors[1].get_angle())),0,self.UPPER_ARM*np.cos(np.radians(self.motors[1].get_angle()))],
                [np.sin(np.radians(self.motors[1].get_angle())),np.cos(np.radians(self.motors[1].get_angle())),0,self.UPPER_ARM*np.sin(np.radians(self.motors[1].get_angle()))],
                [0,0,1,0],
                [0,0,0,1] ]
        # Matrix for the second frame (I can not explain the math you will have to go learn it)
        H1_2 = [[np.cos(np.radians(self.motors[3].get_angle())),-np.sin(np.radians(self.motors[3].get_angle())),0,self.FOREARM*np.cos(np.radians(self.motors[3].get_angle()))],
                [np.sin(np.radians(self.motors[3].get_angle())),np.cos(np.radians(self.motors[3].get_angle())),0,self.FOREARM*np.sin(np.radians(self.motors[3].get_angle()))],
                [0,0,1,0],
                [0,0,0,1]]
        # Matrix for the third frame (I can not explain the math you will have to go learn it)
        H2_3 = [[np.cos(np.radians(self.motors[5].get_angle())),-np.sin(np.radians(self.motors[5].get_angle())),0,self.WRIST*np.cos(np.radians(self.motors[1].get_angle()))],
                [np.sin(np.radians(self.motors[5].get_angle())),np.cos(np.radians(self.motors[5].get_angle())),0,self.WRIST*np.sin(np.radians(self.motors[1].get_angle()))],
                [0,0,1,0],
                [0,0,0,1]]
        # Matrix for entire arm (I can not explain the math you will have to go learn it)
        self.H0_3 = np.dot(np.dot(H0_1,H1_2),H2_3)
        print(np.matrix(self.H0_3))

    def calibrate(self,show_pos=False):
        for motor in self.motors:
            if show_pos:
                self.q.put((motor.get_position,[]))
                print(self.returns.get())
            self.q.put((motor.get_angle,[]))
            self.home_angle.append(self.returns.get())

    def home(self):
        for i in reversed(range(0,len(self.motors))):
            if i != 2 and i != 4:
                self.q.put((self.motors[i].set_angle,[self.home_angle[i]]))
                time.sleep(.06)

    def set_base(self,angle,show_pos=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        position = angle * (1023/300)
        if show_pos:
            print(int(position))
        self.q.put((self.motors[0].set_angle,[angle]))

    def set_shoulder(self,angle,show_pos=False,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 59
        if angle < 58 or angle > 240:
            print("Out of range")
        else:
            self.q.put((self.motors[1].set_angle,[angle]))

    def set_elbow(self,angle,show_pos=False,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 60
        if angle < 58 or angle > 264:
            print("Out of range")
        else:
            self.q.put((self.motors[3].set_angle,[angle]))

    def set_wrist_vertical(self,angle,show_pos=False,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 57
        if angle < 54 or angle > 244:
            print("Out of range")
        else:
            self.q.put((self.motors[5].set_angle,[angle]))

    def set_wrist_angle(self,angle,show_pos=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        self.q.put((self.motors[6].set_angle,[angle]))

    def hand(self,state=""):
        if state != "":
            if state == "open":
                self.q.put((self.motors[-1].set_angle,[150]))
            if state == "close":
                self.q.put((self.motors[-1].set_angle,[0]))

    def full_extend(self):
        self.set_elbow(240)
        time.sleep(.15)
        self.set_shoulder(150)
        self.set_wrist_vertical(150)

    def move(self,x,y,z,phi=270):
        theta_1 = np.arctan2(y,x)
        if True:
            b = np.sqrt((x**2 + z**2))
            a = np.sqrt(b**2+self.WRIST**2)
            beta = np.arccos((b**2 + a**2 - self.WRIST**2 )/(2*a*b))
            alpha = np.arccos((self.UPPER_ARM**2 + a**2 - self.FOREARM**2 )/(2*a*self.UPPER_ARM))
            theta_3 = np.arccos((self.UPPER_ARM**2 + self.FOREARM**2 - a**2)/(2*self.FOREARM*self.UPPER_ARM))
            # c = np.sqrt(x**2+self.BASE_HEIGHT**2)
            gamma = np.arctan2(z,x)
            theta_2 = np.pi-(alpha + beta + gamma)
            theta_4 = 2*np.pi - (np.deg2rad(phi) + theta_3 - (alpha + beta + gamma))
            print("Base: " + str(np.degrees(theta_1)))
            print("Shoulder: " + str(np.degrees(theta_2)))
            print("Elbow: " + str(np.degrees(theta_3)))
            print("Wrist: " + str(np.degrees(theta_4)))
            self.set_base(theta_1,radians=True)
            self.set_shoulder(theta_2,radians=True)
            self.set_elbow(theta_3,radians=True)
            time.sleep(.01)
            time.sleep(.01)
            self.set_wrist_vertical(theta_4,actual=True,radians=True)

        else:
            print("Base position can not be between 299 and 360 degrees.")


# start_time = time.time()
arm = RobotArm()
# end_time = time.time()

# print(end_time-start_time)
