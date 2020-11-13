import time
import VL53L0X

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

while True:
    D = tof.get_distance()

    print(D)
    time.sleep(1)
