import time
import random
import Sensing.ColorSensingFinal as sen
import Arm_Manipulation.Robot_Arm as am
# import IR_Sensor.IR_Sensor as ir

arm = am.RobotArm()


base_angle = [103,120,141,168,185]
colors = ["red","orange","yellow","green","blue"]



positions = {}


color_check = {
    base_angle[0]:[5.6,.95],
    base_angle[1]:[4.15,.75],
    base_angle[2]:[3.35,.75],
    base_angle[3]:[3.45,.5],
    base_angle[4]:[5,.5]

}

coords = {
    base_angle[0]:[7.15,.75],
    base_angle[1]:[5.55,.25],
    base_angle[2]:[5.65,.25],
    base_angle[3]:[5.15,.25],
    base_angle[4]:[6.15,.75]
}

def find_locations():
    for angle in color_check:
        arm.set_base(angle)
        time.sleep(1)
        arm.move(color_check[angle][0],color_check[angle][1])
        time.sleep(1)
        positions[sen.whoDis()] = angle
        arm.move(5,4)

# def check_angle():
#     left,right = ir.get_range()
#     if right < 100:
#         arm.set_wrist_angle(-40)

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def check():
    for color in colors:
        try:
            positions[color]
        except:
            temp = []
            for key in positions:
                temp.append(positions[key])
            missing = Diff(base_angle,temp)
            positions[color] = missing

def stack():
    # random.shuffle(colors)
    # print(colors)
    for color in colors:
        angle = positions[color]
    # for angle in base_angle:
        arm.set_wrist_angle(arm.home_angle[-2],actual=True)
        arm.set_base(angle)
        time.sleep(1)
        arm.move(coords[angle][0],2)
        # check_angle()
        arm.hand_open()
        time.sleep(1.5)
        arm.move(coords[angle][0],coords[angle][1])
        arm.hand_close()
        time.sleep(1)
        arm.move(coords[angle][0],4.25)
        arm.set_base(220)
        time.sleep(.85)
        arm.move(6.2,0)
        arm.hand_open()
        time.sleep(1)
        arm.move(5,4)
        arm.hand_close()

find_locations()
check()
print(positions)
stack()
