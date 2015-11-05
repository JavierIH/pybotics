import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('examples', '')))

import smbus
from driver.pca9685.pca9685 import ServoController
import time

bus = smbus.SMBus(0)

device_address = 0x40

if not bus:
    raise Exception('I2C bus connection failed!')

servo_id = 4
servo_trim = 0

control = ServoController(bus, device_address)
control.setFrequency(60)

control.addServo(servo_id, servo_trim)

while True:
    control.move(servo_id, 20)
    print 'moving to 20'
    time.sleep(1)

    control.move(servo_id, -20.0)
    print 'moving to -20'
    time.sleep(1)
