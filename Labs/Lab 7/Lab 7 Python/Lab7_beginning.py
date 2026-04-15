from scamp import *

import comms, utils, init
from pynput import keyboard
import threading, math, random
import tkinter as tk

from setup import *
import tkinter as tk
from plotData import MultiGraph
from imu_processing import *

root = tk.Tk()
gui = MultiGraph(root)

debug = False # set to True to monitor incoming midi messages
MONITOR = 'angles' # 'accel', 'gyro', 'magnitude', 'tilt', 'angles'

# handlers for incoming midi messages
# also remember, we are storing them in the active_notes and ccs arrays
def handle_note(note, velocity):
    if debug: print('note', note, velocity)
    
accel_vals = [0,0,0]
gyro_vals = [0,0,0]
def handle_cc(num, val):
    if debug: print('cc', num, val)
    
    # IMU data is two 7-bit values combined for 14-bits.
    if 0 <= (num-32) < 3:
        accel_vals[num - 32] = val/127
        accel_vals[num - 32] += ccs[num-32]    
    elif 0 <= (num-32-3) < 3:
#         print(num - 32 - 3, val)
        val = val*1
        gyro_vals[num - 32 - 3] = val/127
        gyro_vals[num - 32 - 3] += ccs[num-32]
        gyro_vals[num - 32 - 3] -= 64
    
    process_imu_data()
    
# here we take our imu data and use the functions in imu_processing
magnitude = [0]
angles = [0,0,0,]
tilt = [0,0,0,]
def process_imu_data():
    global magnitude, tilt, angles
    tilt = get_tilt_angles(accel_vals)
    magnitude = get_magnitude(accel_vals)
#     print(magnitude)
    angles = get_gyro_angles(gyro_vals)
#     print(angles)
    pass
    

# main loop
def mainLoop():
    global index, magnitude, tilt, angles
    
    while True:
        # here we can visualize our data
        if MONITOR == 'accel': gui.update(accel_vals)
        if MONITOR == 'gyro': gui.update(gyro_vals)
        if MONITOR == 'magnitude': gui.update(magnitude)
        if MONITOR == 'tilt': gui.update(tilt)
        if MONITOR == 'angles': gui.update([ angles[i]+64 for i in range(3)])
#             
#         # here we can send sequenced data

        wait(0.125) #this time is in fractions of a beat, e.g. 1/64 of a beat
    
def run_session():
    s.fork(mainLoop)
    s.wait_forever()


        
comms.handle_cc = handle_cc
comms.handle_note = handle_note
s.register_midi_listener(comms.esp32_midi_port, comms.handle_midi)

mainLoop()

