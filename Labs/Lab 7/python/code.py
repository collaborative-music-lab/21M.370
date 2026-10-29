# IMU Exploration

import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi, data # custom 21M.370 modules


DEBUG = True

# PD PARAMETERS
midi.send_param("bandpass-filter", 1, "CUTOFF", 0)
midi.send_param("bandpass-filter", 1, "RES", 40)
midi.send_param("bandpass-filter", 1, "DRIVE", 50)
midi.send_param("combfilter", 1, "DELAY", 50)
midi.send_param("combfilter", 1, "FEEDBACK", 90)
midi.send_param("combfilter", 1, "DRIVE", 90)
midi.send_param("basic-lfo", 4, "FREQ", 60)


### IMU SETUP ###
# lsm6 = sensors.IMU(board_type="LSM6")
lsm6 = sensors.IMU(board_type="BMI160")

imu = data.IMUProcessing() #create an instance of our IMUProcessing class

# higher alpha values for smoothing are LESS smoothing. . .
# alpha can be one value for both rising and falling signals
# or an array [0.9, 0.1] to have different smoothing for rising and falling signals
imu.accel_smoothing = 0.5
imu.tilt_smoothing = 0.5
imu.magnitude_smoothing = [0.9,0.1]
imu.jerk_smoothing = 0.1
# imu.angle_smoothing = 1


### TIMER SETUP ####
bpm = 90

event_timer = 0
control_timer = 0
clock_timer = 0
index = 0

event_interval = 0.02 if DEBUG else 0.001
control_interval = 0.2 if DEBUG else 0.02
clock_interval = 60/bpm/4

### MAIN LOOP ###
while True:

    if time.monotonic()-event_timer >= event_interval:
        event_timer = time.monotonic()
        
        # update IMU
        status = lsm6.update()
        if status:
            imu.update( lsm6.accel_cur, lsm6.gyro_cur)
            
    if time.monotonic()- control_timer >= control_interval:
        control_timer = time.monotonic()
        
        # monitor messages here!
        if DEBUG:
            print(imu.accel)
#             print(imu.gyro)
#             print(imu.tilt)
#             print(imu.angle)
#             print(imu.magnitude)
#             print(imu.jerk)
            
            
        x_amplitude = data.scale( abs(imu.tilt[0]), 0, 90, 0, 127)
        y_amplitude = data.scale( abs(imu.tilt[0]), 0, 90, 0, 127)
        z_amplitude = data.scale( abs(imu.tilt[0]), 0, 90, 0, 127)
        
        midi.send_message("voice", 0, "vca", x_amplitude * imu.magnitude )
        midi.send_message("voice", 1, "vca", x_amplitude * imu.magnitude )
        midi.send_message("voice", 2, "vca", x_amplitude * imu.magnitude )
        
        midi.send_message("voice", 0, "pitch", data.scale( (imu.angle[0]), -10, 10, 0, 60))
        midi.send_message("voice", 1, "pitch", data.scale((imu.angle[1]), -10, 10, 0, 60))
        midi.send_message("voice", 2, "pitch", data.scale((imu.angle[2]), -10, 10, 0, 60))
        

    if time.monotonic()-clock_timer >= clock_interval:
        clock_timer = time.monotonic()
        
        index = (index+1) % 32
        if index == 0:
            imu.angle = [0,0,0]
            print('reset angles')


