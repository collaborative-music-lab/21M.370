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

for m in init.initial_params:
    comms.send_osc(*m)

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
    

# main loop
def mainLoop():
    global magnitude, tilt, angles
    index = 0
    notes_pressed = 0
    
    while True:
        # generate some rhythms!
        
        # use tilt to change rhythms
        rhythmA = math.floor( utils.scale( tilt[0], 20,50, 2,8) )
        rhythmA = max( 1, rhythmA )
        rhythmB = math.floor( utils.scale( tilt[1], 20,50, 20,48) )
        rhythmC = math.floor( utils.scale( tilt[2], 20,50, 0,6) )
        
        amplitude = max( magnitude[0]-40, 0)
        amplitude = utils.scale( amplitude, 0,80, 0, 127)
        amplitude = mag_onepole.update(amplitude)
        comms.send_osc("vca", 1, "CV", amplitude)
        
        # if a button is pressed use angle to change parameters
        if len(active_notes) > 0:
            if notes_pressed == 0:
                reset_gyro_angle()
                notes_pressed = 1
            decay = utils.clip( utils.scale( angles[0], 0,90, 0, 80), 0, 127)
            decay = math.floor( decay )
            cutoff = utils.clip( utils.scale( angles[1], -45, 45, 10,128) )
            cutoff = math.floor( cutoff )
            lfo_depth = utils.clip( utils.scale( angles[2], 0,-90, 20, 120) ,0,127 )
            lfo_depth = math.floor( lfo_depth )
            lfo_rate = utils.clip( utils.scale( angles[2], 0,-90, 50,90) ,0,127 )
            lfo_rate = math.floor( lfo_rate )
#             print( "decay: ", decay)
#             print( "cuitoff: ", cutoff)
#             print( "lfo: ", lfo_depth, lfo_rate)
            comms.send_osc("decay", 1, "D", decay )
            comms.send_osc("analog-filter", 1, "CUTOFF", cutoff )
            comms.send_osc("basic-lfo", 0, "DEPTH", lfo_depth )
            comms.send_osc("basic-lfo", 0, "FREQ", lfo_rate )
        else: notes_pressed = 0
            
        
        decay = math.pow( index%64%20/32, 2) * .3 + 0.0
        if index%64% rhythmA > 3: comms.send_osc("voice", 0, "trigger", decay)
        if index%34%rhythmB%4 == 0: comms.send_osc("voice", 1, "trigger", decay)
        if index%8%3: comms.send_osc("voice", 2, "trigger", decay+1-.5)
        if index%128%90%6 > rhythmC: comms.send_osc("voice", 3, "trigger", decay)
        
        index = index+1
        
        # here we can visualize our data
        if MONITOR == 'accel': gui.update(accel_vals)
        if MONITOR == 'gyro': gui.update([ gyro_vals[i]+64 for i in range(3)])
        if MONITOR == 'magnitude': gui.update(magnitude)
        if MONITOR == 'tilt': gui.update(tilt)	
        if MONITOR == 'angles': gui.update([ angles[i]+64 for i in range(3)])


        wait(0.125) #this time is in fractions of a beat, e.g. 1/64 of a beat
    
def run_session():
    s.fork(mainLoop)
    s.wait_forever()

        
comms.handle_cc = handle_cc
comms.handle_note = handle_note
s.register_midi_listener(comms.esp32_midi_port, comms.handle_midi)

mainLoop()


