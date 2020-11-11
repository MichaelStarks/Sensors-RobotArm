import time
import random
from Robot_Arm import RobotArm

arm = RobotArm()


base_angle = [107,124,145,171,187]
colors = ["Red","Blue","Green","Yellow","Orange"]

positions = {}

coords = {
    107:[6.75,.75],
    124:[5.5,.25],
    145:[5,.25],
    171:[5.25,.25],
    187:[6.5,.75]
}

# arm.hand()
def find_locations():
    for angle in base_angle:
        arm.set_base(angle)
        time.sleep(.5)
        arm.move(coords[angle][0]-1,2)
        time.sleep(1.5)
        # Get color at position and add to dic

def stack():
    random.shuffle(colors)
    print(colors)
    for color in colors:
        angle = positions[color]
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
