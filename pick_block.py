import time
from Robot_Arm_no_threads import RobotArm

arm = RobotArm()

time.sleep(2)
arm.set_base(16)
arm.hand()
arm.set_wrist_angle(135)
time.sleep(1)
arm.move(5,.5)
time.sleep(1.5)
arm.hand()
arm.move(5,4)
time.sleep(1.5)
arm.set_base(arm.home_angle[0])
time.sleep(1.5)
arm.move(9,.75)
time.sleep(1.5)
arm.hand()
time.sleep(1.5)
arm.move(9,2)
time.sleep(1.5)
arm.move(5,4)
