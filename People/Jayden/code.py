# Jayden Lin

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
lsm6 = sensors.IMU(board_type="LSM6")
# lsm6 = sensors.IMU(board_type="BMI160")

imu = data.IMUProcessing() #create an instance of our IMUProcessing class

# higher alpha values for smoothing are LESS smoothing. . .
# alpha can be one value for both rising and falling signals
# or an array [0.9, 0.1] to have different smoothing for rising and falling signals
imu.accel_smoothing = 0.5
imu.tilt_smoothing = 0.5
imu.magnitude_smoothing = [0.9,0.1]
imu.jerk_smoothing = 0.1
# imu.angle_smoothing = 1


### JERK -> PITCH SETTINGS ###
JERK_MAX = 1.0     # tune this: roughly the biggest jerk printed when shaking hard
LOW_PITCH = 30     # pitch when still
HIGH_PITCH = 90    # pitch at maximum jerk


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
            print(imu.jerk)
#             print(imu.accel)
#             print(imu.gyro)
#             print(imu.tilt)
#             print(imu.angle)
#             print(imu.magnitude)
            
            
        x_amplitude = data.scale( abs(imu.tilt[0]), 0, 90, 0, 127)
        y_amplitude = data.scale( abs(imu.tilt[0]), 0, 90, 0, 127)
        z_amplitude = data.scale( abs(imu.tilt[0]), 0, 90, 0, 127)
        
        # jerk -> pitch: still = low pitch, jerky = high pitch
        j = imu.jerk
        if isinstance(j, (list, tuple)):   # if jerk is per-axis, use the biggest axis
            j = max(abs(v) for v in j)
        j = min(abs(j), JERK_MAX)          # clamp so pitch can't overshoot
        jerk_pitch = data.scale(j, 0, JERK_MAX, LOW_PITCH, HIGH_PITCH)
            
        midi.send_message("voice", 0, "vca", x_amplitude * imu.magnitude )
        midi.send_message("voice", 1, "vca", x_amplitude * imu.magnitude )
        midi.send_message("voice", 2, "vca", x_amplitude * imu.magnitude )
        
        midi.send_message("voice", 0, "pitch", jerk_pitch)
        midi.send_message("voice", 1, "pitch", jerk_pitch)
        midi.send_message("voice", 2, "pitch", jerk_pitch)
        

    if time.monotonic()-clock_timer >= clock_interval:
        clock_timer = time.monotonic()
        
        index = (index+1) % 32
        if index == 0:
            imu.angle = [0,0,0]
            print('reset angles')