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
        self.lock = self.robot_arm_dxl.lock
        self.BASE_HEIGHT = 4.3897638
        self.UPPER_ARM = 5.6929134
        self.FOREARM = 5.6889764
        self.WRIST = 5.4015748
        for i in range(1,9):
            # print(i)
            self.motors.append(self.robot_arm_dxl.new_ax12(i))
            self.motors[-1].manual_write_lock().torque_enable()
            self.motors[-1].manual_write_lock().set_position_mode()
        # self.set_elbow(0)
        with self.lock:
            self.calibrate()
        self.motors[2].manual_write_lock().set_velocity_mode()
        self.motors[4].manual_write_lock().set_velocity_mode()
        __shoulder_thread__ = threading.Thread(target=self.__motor_assist_shoulder__, args=(),daemon=True)
        __shoulder_thread__.start()
        __elbow_thread__ = threading.Thread(target=self.__motor_assist_shoulder__, args=(),daemon=True)
        __elbow_thread__.start()

        # self.__denavit_hartenberg_maritx__()


    def __del__(self):
        for motor in self.motors:
            motor.torque_disable()


    def __motor_assist_shoulder__(self):
        velocity = 512
        current_shoulder = 0
        goal_shoulder = 0
        while True:
            direction_shoulder = 0
            with self.lock:
                current_shoulder = self.motors[1].manual_read_lock().get_position()
                goal_shoulder = self.motors[1].manual_read_lock().read_control_table("Goal_Position")
                if abs(goal_shoulder - current_shoulder) < 5:
                    direction_shoulder = 0
                else:
                    print(True)
                    direction_shoulder = (goal_shoulder-current_shoulder)/abs(goal_shoulder-current_shoulder)
                self.motors[2].manual_write_lock().set_velocity(-int(direction_shoulder*velocity))

    def __motor_assist_elbow__(self):
        velocity = 512
        current_elbow = 0
        goal_elbow = 0
        while True:
            direction_elbow = 0
            with self.lock:
                current_elbow = self.motors[3].manual_read_lock().get_position()
                goal_elbow = self.motors[3].manual_read_lock().read_control_table("Goal_Position")
                if abs(goal_elbow - current_elbow) < 5:
                    direction_elbow = 0
                else:
                    direction_elbow = (goal_elbow-current_elbow)/abs(goal_elbow-current_elbow)
                self.motors[4].manual_write_lock().set_velocity(-int(direction_elbow*velocity))

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
                print(motor.manual_read_lock().get_position())
            self.home_angle.append(motor.manual_read_lock().get_angle())

    def home(self):
        with self.lock:
            for i in reversed(range(0,len(self.motors))):
                if i != 2 and i != 4:
                    self.motors[i].manual_write_lock().set_angle(self.home_angle[i])
                    time.sleep(.06)

    def set_base(self,angle,show_pos=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        position = angle * (1023/300)
        with self.lock:
            if show_pos:
                print(int(position))
            self.motors[0].manual_write_lock().set_angle(angle)

    def set_shoulder(self,angle,show_pos=False,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 59
        if angle < 58 or angle > 240:
            print("Out of range")
        else:
            with self.lock:
                self.motors[1].manual_write_lock().set_angle(angle)

    def set_elbow(self,angle,show_pos=False,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 60
        if angle < 58 or angle > 264:
            print("Out of range")
        else:
            with self.lock:
                self.motors[3].manual_write_lock().set_angle(angle)

    def set_wrist_vertical(self,angle,show_pos=False,actual=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        if not actual:
            angle = angle + 57
        if angle < 54 or angle > 244:
            print("Out of range")
        else:
            with self.lock:
                self.motors[5].manual_write_lock().set_angle(angle)

    def set_wrist_angle(self,angle,show_pos=False,radians=False):
        if radians:
            angle = np.degrees(angle)
        with self.lock:
            self.motors[6].manual_write_lock().set_angle(angle)

    def hand(self,state=""):
        angle = 0
        if state != "":
            if state == "open":
                angle = 150
            if state == "close":
                angle = 0
            self.motors[-1].manual_write_lock().set_angle(angle)

    def full_extend(self):
        with self.lock:
            self.set_elbow(240)
            time.sleep(.15)
            self.set_shoulder(150)
            self.set_wrist_vertical(150)

    # def move(self,x,y,z,phi=270):
    #     with self.lock:
    #         theta_1 = np.arctan2(y,x)
    #         if True:
    #             b = np.sqrt((x**2 + z**2))
    #             a = np.sqrt(b**2+self.WRIST**2)
    #             beta = np.arccos((b**2 + a**2 - self.WRIST**2 )/(2*a*b))
    #             alpha = np.arccos((self.UPPER_ARM**2 + a**2 - self.FOREARM**2 )/(2*a*self.UPPER_ARM))
    #             theta_3 = np.arccos((self.UPPER_ARM**2 + self.FOREARM**2 - a**2)/(2*self.FOREARM*self.UPPER_ARM))
    #             # c = np.sqrt(x**2+self.BASE_HEIGHT**2)
    #             gamma = np.arctan2(z,x)
    #             theta_2 = np.pi-(alpha + beta + gamma)
    #             theta_4 = 2*np.pi - (np.deg2rad(phi) + theta_3 - (alpha + beta + gamma))
    #             print("Base: " + str(np.degrees(theta_1)))
    #             print("Shoulder: " + str(np.degrees(theta_2)))
    #             print("Elbow: " + str(np.degrees(theta_3)))
    #             print("Wrist: " + str(np.degrees(theta_4)))
    #             self.set_base(theta_1,radians=True)
    #             self.set_shoulder(theta_2,radians=True)
    #             self.set_elbow(theta_3,radians=True)
    #             time.sleep(.01)
    #             time.sleep(.01)
    #             self.set_wrist_vertical(theta_4,actual=True,radians=True)
    #
    #         else:
    #             print("Base position can not be between 299 and 360 degrees.")
    def move(self,x,z,phi=180):
        alpha = np.tan(self.BASE_HEIGHT/x)
        beta = 90 - alpha
        b = np.sqrt(z**2+x**2-2*z*x*np.cos(beta))
        omega = np.arctan((self.WRIST + (z-self.BASE_HEIGHT))/x)
        zeta = np.arccos((b**2+x**2-(z-self.BASE_HEIGHT)**2)/(2*b*x))
        delta = omega - zeta
        c = self.WRIST/np.arccos(delta)
        theta_2 = np.arccos((self.UPPER_ARM**2 + self.FOREARM**2 - c**2)/(2*self.UPPER_ARM*self.FOREARM))
        epsilon = np.arccos((c**2+self.UPPER_ARM**2-self.FOREARM**2)/(2*c*self.UPPER_ARM))
        theta_1 = np.pi - delta - epsilon-zeta
        theta_3 = np.deg2rad(phi) - epsilon-delta-zeta-theta_2
        print("Shoulder: " + str(np.degrees(theta_1)))
        print("Elbow: " + str(np.degrees(theta_2)))
        print("Wrist: " + str(np.degrees(theta_3)))
        self.set_elbow(theta_2,radians=True)
        self.set_shoulder(theta_1,radians=True)
        self.set_wrist_vertical(theta_3,radians=True)


# start_time = time.time()
arm = RobotArm()
# end_time = time.time()

# print(end_time-start_time)
