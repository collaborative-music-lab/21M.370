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
MONITOR = 'accel' # 'accel', 'gyro', 'magnitude', 'tilt', 'angles'

for m in init.initial_params:
    comms.send_osc(*m)
    
comms.send_osc('slope', 2, 'RISE', 10)
comms.send_osc('slope', 2, 'FALL', 50)
comms.send_osc('analog-filter', 1, 'CUTOFF', 40)
comms.send_osc('analog-filter', 1, 'Q', 60)
comms.send_osc('vca', 1, 'CV', 60)

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
mag_onepole = utils.OnePole(.3)
angles = [0,0,0,]
tilt = [0,0,0,]
def process_imu_data():
    global magnitude, tilt, angles
    tilt = get_tilt_angles(accel_vals)
    magnitude = get_magnitude(accel_vals)
    angles = get_gyro_angles(gyro_vals)
    pass
    

def pitch2midi(val):
    scale = [0,2,3,5,7,9,10]
    octave = math.floor(val/len(scale))
    degree = (val +len(scale)*7)% len(scale)
    degree = scale[degree]
    return degree + octave*12

# main loop
def mainLoop():
    global magnitude, tilt, angles
    index = 0
    
    sequence = [0,2,4,6,4,2,3,5,7,9,7,5, 1,3,5,7,5,3,1,3,5,7,9,7]
    
    while True:
        # generate some rhythms!
        pitch = pitch2midi( sequence[index % len(sequence)] ) 
        comms.send_osc("voice", index%8, "pitch", (pitch+36 + index%3*12)/127)
        comms.send_osc("voice", index%8, "trigger", .5)
        
        index = index+1
        
        
        # here we can visualize our data
        if MONITOR == 'accel': gui.update(accel_vals)
        if MONITOR == 'gyro': gui.update([ gyro_vals[i]+64 for i in range(3)])
        if MONITOR == 'magnitude': gui.update(magnitude)
        if MONITOR == 'tilt': gui.update(tilt)
        if MONITOR == 'angles': gui.update([ angles[i]+64 for i in range(3)])

        print(index)
        wait(.5) #this time is in fractions of a beat, e.g. 1/64 of a beat
    
def run_session():
    s.fork(mainLoop)
    s.wait_forever()

        
comms.handle_cc = handle_cc
comms.handle_note = handle_note
s.register_midi_listener(comms.esp32_midi_port, comms.handle_midi)

mainLoop()



