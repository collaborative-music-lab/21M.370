#####
# Code for using the M5stick as a wireless IMU

# Make sure to set the channel number in imu2.py to match the number shown on the m5 display
####

import board
import time, math
import analogio
import digitalio
import neopixel
import imu2


#local files to import
from imu_driver import IMU
from imu_processing import *
import utils, midi, setup

DEBUG = True
DATA_TO_SEND = ['accel','gyro']
DATA_RATE = 20 # ms interval between sending data


# to double our resolution we are going to use two ccs per axis
# cc[base] will handle the upper 7 bits
# cc[base+32] will handle the lower 7 bits
def sendImuData(type, vals):
    # Base CC numbers # Accel: X=0, Y=1, Z=2 # Gyro:  X=3, Y=4, Z=5
    base_cc = 0 if type == 'accel' else 3
    
    # Define the sensor physical range for scaling
    # Assuming accel is +/- 2g and gyro is +/- 250 dps (adjust as needed)
    limit = 2.0 if type == 'accel' else 250.0 

    for i in range(3):
        # 1. Scale raw value to 14-bit unsigned integer (0 - 16383)
        
        full_val = int(utils.scale(vals[i], -limit, limit, 0, 16383)) # Mapping -limit to 0 and +limit to 16383
        full_val = max(0, min(16383, full_val)) # Clamp value to ensure it stays in 14-bit range

        # Split into MSB and LSB
        msb = (full_val >> 7) & 0x7F
        lsb = full_val & 0x7F

        # Send MIDI CCs
        # use midi.force_send_cc to make sure data is sent every time
        cc_num = base_cc + i
        midi.force_send_cc(cc_num, msb)        # Coarse / MSB
        midi.force_send_cc(cc_num + 32, lsb)   # Fine / LSB (Offset 32)
        if DEBUG: print(type, cc_num, full_val)

# use led for status monitoring
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

# two separate timers to do sensor reading and midi sending
read_timer = time.monotonic()
serial_timer = time.monotonic()
current_time = time.monotonic()


# main loop
# the send_delay prevents random data being sent when the mpr121 is reset
send_delay =  time.monotonic() + 3

while True:
    current_time = time.monotonic()
    send_midi = True
    if current_time > send_delay: send_midi = True
    imu2.update()
    time.sleep(0.01)
        
    # send CC data and check for incoming midi
    if (current_time - serial_timer) >= DATA_RATE/1000:
        serial_timer = current_time

#         print( get_tilt_angles(accel) )
        accel = imu2.accel
        gyro = imu2.gyro
        
        # print(accel, gyro)
        
        if 'accel' in DATA_TO_SEND: sendImuData('accel', accel)
        if 'gyro' in DATA_TO_SEND: sendImuData('gyro', gyro)
        
        if midi.check_input():
                pixel.fill((100, 0, 0))
                send_delay =  time.monotonic() + 3
        elif send_midi: pixel.fill((0, 100, 0))
        else:  pixel.fill((0, 0, 100))
        

