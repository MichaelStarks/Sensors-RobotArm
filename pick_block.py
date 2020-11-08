import time
from Robot_Arm_no_threads import RobotArm

arm = RobotArm()


base_angle = [0,25,45,60]

positions = {
    0:[5,.75],
    25:[5,.75],
    45:[5.5,.75],
    60:[7,.75]
}

# arm.hand()
def find_locations():
    for angle in base_angle:
        arm.set_base(angle)
        time.sleep(.5)
        arm.move(positions[angle][0]-1,2)
        time.sleep(1.5)
        # Get color at position and add to dic

def stack():
    for angle in base_angle:
        arm.set_base(angle)
        time.sleep(.5)
        arm.move(positions[angle][0],4.5)
        arm.hand_open()
        time.sleep(1)
        arm.move(positions[angle][0],positions[angle][1])
        time.sleep(.5)
        arm.hand_close()
        time.sleep(1)
        arm.move(positions[angle][0],2.5)
        time.sleep(1)
        arm.set_base(arm.home_angle[0])
        time.sleep(1)
        arm.move(8,1.25)
        time.sleep(1)
        arm.hand_open()
        time.sleep(1)
        arm.move(8,2.5)
        arm.hand_close()
        time.sleep(5)
        # Get color at position and add to dic

find_locations()
stack()
