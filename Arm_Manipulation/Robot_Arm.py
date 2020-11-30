import time
import math
import numpy as np
from dynio import *


class RobotArm:

    def __init__(self):
        self.current_x = 0
        self.current_z = 0
        self.motors = [] # Motors are ordered from bottem to top
        self.home_angle = [] # Motors are ordered from bottem to top
        self.robot_arm_dxl = None
        self.robot_arm_dxl = dxl.DynamixelIO("/dev/ttyUSB0")
        self.BASE_HEIGHT = 4.07
        self.UPPER_ARM = 5.7165354
        self.FOREARM = 5.7165354
        self.WRIST = 6.10236
        for i in range(1,9):
                self.motors.append(self.robot_arm_dxl.new_ax12(i))
                self.motors[-1].set_position_mode(goal_current=512)
                self.motors[-1].torque_enable()
        self.calibrate()
        for i in range(1,len(self.motors)):
            self.motors[i].set_position_mode(goal_current=475)
        self.set_base(140)
        time.sleep(.5)
        self.move(5,4)
        self.hand_close()

    def __del__(self):
        for motor in self.motors:
            motor.torque_disable()

    def calibrate(self,show_pos=False):
        for motor in self.motors:
            if show_pos:
                print(motor.get_position())
            self.home_angle.append(motor.get_angle())

    def home(self):
        for i in reversed(range(0,len(self.motors))):
            self.motors[i].set_angle(self.home_angle[i])
            time.sleep(.01)

    def set_base(self,angle,show_pos=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if show_pos:
            position = angle * (1023/300)
            print(int(position))
        direction = -(self.motors[0].get_angle() - (angle+1))/abs(self.motors[0].get_angle() - (angle+1))
        for move_angle in np.arange(self.motors[0].get_angle(),angle+1,2*direction):
            self.motors[0].set_angle(move_angle)

    def set_shoulder(self,angleRef,radians=False):
        direction = -(self.motors[1].get_angle() - (angleRef+60))/abs(self.motors[1].get_angle() - (angleRef+60))
        for move_angle in np.arange(self.motors[1].get_angle(),angleRef+60,2*direction):
            self.motors[1].set_angle(move_angle)
            self.motors[2].set_angle(self.home_angle[2]-(move_angle-60))

    def set_elbow(self,angleRef,radians=False):
        direction = -(self.motors[3].get_angle() - (angleRef+60))/abs(self.motors[1].get_angle() - (angleRef+60))
        for move_angle in np.arange(self.motors[3].get_angle(),angleRef+60,2*direction):
            self.motors[3].set_angle(move_angle)
            self.motors[4].set_angle(self.home_angle[4]-(move_angle-60))

    def set_wrist_vertical(self,angle,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 54
        if angle < 54 or angle > 244:
            print("Out of range wrist")
        else:
            direction = -(self.motors[5].get_angle() - (angle+1))/abs(self.motors[5].get_angle() - (angle+1))
            for move_angle in np.arange(self.motors[5].get_angle(),angle+1,3*direction):
                self.motors[5].set_angle(move_angle)

    def set_wrist_angle(self,angle,actual=False,show_pos=False):
        direction = -(self.motors[6].get_angle() - (angle+1))/abs(self.motors[6].get_angle() - (angle+1))
        for move_angle in np.arange(self.motors[6].get_angle(),angle+1,direction):
            self.motors[6].set_angle(move_angle)

    def hand_close(self):
        self.motors[-1].set_velocity_mode()
        self.motors[-1].set_velocity(-512)
        time.sleep(.15)
        while(abs(self.motors[-1].read_control_table("Present_Speed")) != 0):
            continue
        self.motors[-1].set_velocity(0)

    def hand_open(self):
        self.motors[-1].set_position_mode()
        self.motors[-1].set_angle(150)

    def full_extend(self):
        self.set_elbow(240)
        time.sleep(.15)
        self.set_shoulder(150)
        self.set_wrist_vertical(150)

    def ___sync_motors__(self):
        self.motors[4].set_angle(self.motors[4].get_angle())
        self.motors[2].set_angle(self.motors[2].get_angle())

    def move(self,x,z,phi=180):
        z = z + 1.75
        a = np.sqrt(self.BASE_HEIGHT**2 + x**2)
        alpha = np.tan(x/self.BASE_HEIGHT)
        c = np.sqrt(x**2 + (self.WRIST+(z-self.BASE_HEIGHT))**2)
        omega = np.arccos((c**2 + x** 2 - (self.WRIST + (z-self.BASE_HEIGHT))**2)/(2.0*c*x))
        theta_2 = np.arccos((self.UPPER_ARM**2 + self.FOREARM**2 - c**2)/(2.0*self.UPPER_ARM*self.FOREARM)) - np.deg2rad(16)
        epsilon = np.arccos((c**2+self.UPPER_ARM**2-self.FOREARM**2)/(2.0*c*self.UPPER_ARM))
        theta_1 = np.pi - (epsilon + omega) - np.deg2rad(10)
        theta_3 = np.deg2rad(phi) - ((epsilon + omega) + theta_2)
        theta_1 = np.degrees(theta_1)
        theta_2 = np.degrees(theta_2)
        self.set_elbow(theta_2)
        self.set_shoulder(theta_1)
        if theta_3 < 0:
            theta_3 = 0
        self.set_wrist_vertical(theta_3,radians=True)
        time.sleep(2)
        self.___sync_motors__()
        return True
