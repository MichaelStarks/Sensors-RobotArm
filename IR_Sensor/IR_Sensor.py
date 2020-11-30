import time

import board
import busio

import adafruit_vl53l0x

i2c = busio.I2C(board.SCL, board.SDA)
# temp = adafruit_vl53l0x.VL53L0X(i2c)
# temp.set_address(49)
IR_Right = adafruit_vl53l0x.VL53L0X(i2c,address=49)
IR_Left = adafruit_vl53l0x.VL53L0X(i2c,address=48)

def get_range():
    return [IR_Left.range,IR_Right.range]
