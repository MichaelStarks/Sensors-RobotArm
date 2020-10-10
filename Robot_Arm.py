import time
import math
import numpy as np
from dynio import *


class RobotArm:

    def __init__(self):
        self.motors = [] # Motors are ordered from bottem to top
        self.home_angle = [] # Motors are ordered from bottem to top
        self.robot_arm_dxl = None
        self.robot_arm_dxl = dxl.DynamixelIO("/dev/ttyUSB0")
        self.BASE_HEIGHT = 0
        self.UPPER_ARM = 5.6875
        self.FOREARM = 5.6875
        self.WRIST = 5.5
        for i in range(1,9):
                self.motors.append(self.robot_arm_dxl.new_ax12(i))
                self.motors[-1].torque_enable()
                self.motors[-1].set_position_mode(goal_current=980)
        # self.set_elbow(0)
        self.calibrate()
        # self.__denavit_hartenberg_maritx__()


    def __del__(self):
        self.home()

        # Calculates the Denavit-Hartenberg Maritx
    def __denavit_hartenberg_maritx__(self):
        # Matrix for the first frame (I can not explain the math you will have to go learn it)
        H0_1 = [[np.cos(self.motors[1].get_angle()),-np.sin(self.motors[1].get_angle()),0,self.UPPER_ARM*np.cos(self.motors[1].get_angle())],
                [np.sin(self.motors[1].get_angle()),np.cos(self.motors[1].get_angle()),0,self.UPPER_ARM*np.sin(self.motors[1].get_angle())],
                [0,0,1,0],
                [0,0,0,1]]
        # Matrix for the second frame (I can not explain the math you will have to go learn it)
        H1_2 = [[np.cos(self.motors[3].get_angle()),-np.sin(self.motors[3].get_angle()),0,self.FOREARM*np.cos(self.motors[3].get_angle())],
                [np.sin(self.motors[3].get_angle()),np.cos(self.motors[3].get_angle()),0,self.FOREARM*np.sin(self.motors[3].get_angle())],
                [0,0,1,0],
                [0,0,0,1]]
        # Matrix for the third frame (I can not explain the math you will have to go learn it)
        H2_3 = [[np.cos(self.motors[5].get_angle()),-np.sin(self.motors[5].get_angle()),0,self.WRIST*np.cos(self.motors[1].get_angle())],
                [np.sin(self.motors[5].get_angle()),np.cos(self.motors[5].get_angle()),0,self.WRIST*np.sin(self.motors[1].get_angle())],
                [0,0,1,0],
                [0,0,0,1]]
        # Matrix for entire arm (I can not explain the math you will have to go learn it)
        self.H0_3 = np.dot(np.dot(H0_1,H1_2),H2_3)
        print(np.matrix(self.H0_3))

    def calibrate(self,show_pos=False):
        for motor in self.motors:
            if show_pos:
                print(motor.get_position())
            self.home_angle.append(motor.get_angle())

    def home(self):
        for i in reversed(range(0,len(self.motors))):
            self.motors[i].set_angle(self.home_angle[i])
            time.sleep(.01)

    def set_base(self,angle,show_pos=False):
        position = angle * (1023/300)
        if show_pos:
            print(int(position))
        self.motors[0].set_angle(angle)

    def set_shoulder(self,angle,show_pos=False,actual=False):
        if not actual:
            angle = angle + 59
        if angle < 58 or angle > 240:
            print("Out of range")
        else:
            change_angle = abs(self.motors[1].get_angle() - angle)
            self.motors[1].set_angle(angle)
            self.motors[2].set_angle(self.home_angle[2]-change_angle)

    def set_elbow(self,angle,show_pos=False,actual=False):
        if not actual:
            angle = angle + 60
        if angle < 58 or angle > 264:
            print("Out of range")
        else:
            change_angle = abs(self.motors[3].get_angle() - angle)
            self.motors[3].set_angle(angle)
            self.motors[4].set_angle(self.home_angle[4]-change_angle)

    def set_wrist_vertical(self,angle,show_pos=False,actual=False):
        if not actual:
            angle = angle + 57
        if angle < 54 or angle > 244:
            print("Out of range")
        else:
            self.motors[5].set_angle(angle)

    def set_wrist_angle(self,angle,show_pos=False):
        self.motors[6].set_angle(angle)

    def hand(self,state=""):
        if state != "":
            if state == "open":
                self.motors[-1].set_angle(150)
            if state == "close":
                self.motors[-1].set_angle(0)

    def full_extend(self):
        self.set_elbow(240)
        time.sleep(.15)
        self.set_shoulder(150)
        self.set_wrist_vertical(150)

    def move_arm(self,x,y,z):
        theta_one = np.arctan2(y,x)
        if -1 < np.degrees(theta_one) < 300:
            c = z - 5 + self.WRIST*np.sin(np.radians(90))
            A = x - self.WRIST*np.cos(theta_one)*np.cos(np.radians(90))
            B = y - self.WRIST*np.sin(theta_one)*np.cos(np.radians(90))
            theta_three =  np.arccos((A**2+B**2+c**2-self.UPPER_ARM**2-self.FOREARM**2)/(2*self.UPPER_ARM*self.FOREARM))
            a = self.FOREARM*np.sin(theta_three)
            b = self.UPPER_ARM + self.FOREARM*np.cos(theta_three)
            r = np.sqrt(a**2+b**2)
            theta_two = np.arctan2(c,np.sqrt(r**2-c**2)) - np.arctan2(a,b)
            theta_four = np.radians(90) - theta_two - theta_three
            print("Shoulder: " + str(theta_two))
            theta_one = np.degrees(theta_one)
            theta_two = np.degrees(theta_two)
            theta_three = np.degrees(theta_three)
            theta_four = np.degrees(theta_four)
            print("Wrist: " + str(theta_four))
            print("Elbow: " + str(theta_three))
            self.set_base(theta_one)
            self.set_elbow(theta_three)
            time.sleep(.01)
            self.set_shoulder(theta_two)
            time.sleep(.01)
            self.set_wrist_vertical(theta_four)

        else:
            print("Base position can not be between 299 and 360 degrees.")


# start_time = time.time()
arm = RobotArm()
# end_time = time.time()

# print(end_time-start_time)
