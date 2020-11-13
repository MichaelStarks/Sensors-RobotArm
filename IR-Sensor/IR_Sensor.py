import time
import VL53L0X

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)


def get_distance():
    return tof.get_distance()
