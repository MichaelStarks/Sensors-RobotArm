import time
import random
import Sensing.ColorSensingFinal
from Arm_Manipulation.Robot_Arm import RobotArm

arm = RobotArm()


base_angle = [105,125,145,170,185]
colors = ["red","blue","green","yellow","orange"]



positions = {}


color_check = {
    base_angle[0]:[5.75,.75],
    base_angle[1]:[4.5,.5],
    base_angle[2]:[4,.5],
    base_angle[3]:[4,.5],
    base_angle[4]:[5,.5]

}

coords = {
    15:[6.75,.75],
    30:[5.5,.25],
    55:[5,.25],
    80:[5.25,.25],
    96:[6.5,.75]
}

def find_locations():
    for angle in color_check:
        arm.set_base(angle)
        time.sleep(1)
        arm.move(color_check[angle][0],color_check[angle][1])
        time.sleep(1)
        positions.add(whoDis(),angle)
        arm.move(5,4)

def stack():
    # random.shuffle(colors)
    # print(colors)
    # for color in colors:
    #     angle = positions[color]
    for angle in base_angle:
        arm.set_base(angle)
        time.sleep(.25)
        arm.move(coords[angle][0],4.5)
        arm.hand_open()
        time.sleep(.75)
        arm.move(coords[angle][0],coords[angle][1])
        arm.hand_close()
        time.sleep(.5)
        arm.move(coords[angle][0],4.5)
        arm.set_base(146)
        time.sleep(.85)
        arm.move(5.5,0)
        arm.hand_open()
        time.sleep(1)
        arm.move(5,4)
        arm.hand_close()

find_locations()
print(positions)
# stack()
