import time
from Robot_Arm_no_threads import RobotArm

arm = RobotArm()


base_angle = [0,25,45,60]

positions = {
    0:[5.5,.45],
    25:[5.5,.5],
    45:[5.5,.75],
    60:[8,.5]
}

# arm.hand()
def find_locations():
    for angle in base_angle:
        arm.set_base(angle)
        time.sleep(1)
        arm.move(positions[angle][0]-1,1)
        time.sleep(1.5)
        # Get color at position and add to dic

find_locations()
