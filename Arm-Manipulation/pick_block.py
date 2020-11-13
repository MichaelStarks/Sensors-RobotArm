import time
import random
from Robot_Arm import RobotArm

arm = RobotArm()


base_angle = [103,124,140,165,185]
colors = ["Red","Blue","Green","Yellow","Orange"]



positions = {}


color_check = {
    103:[6,.25],
    124:[4.75,.25],
    140:[3.5,.1],
    165:[4,0],
    185:[5,0]

}

coords = {
    103:[6.75,.75],
    124:[5.5,.25],
    140:[5,.25],
    165:[5.25,.25],
    185:[6.5,.75]
}

# arm.hand()
def find_locations():
    for angle in base_angle:
        arm.set_base(angle)
        time.sleep(.5)
        arm.move(color_check[angle][0],color_check[angle][1])
        time.sleep(.75)
        # Get color at position and add to dic
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
        arm.set_base(230)
        time.sleep(.85)
        arm.move(5.5,0)
        arm.hand_open()
        time.sleep(1)
        arm.move(5,4)
        arm.hand_close()

find_locations()
# stack()
