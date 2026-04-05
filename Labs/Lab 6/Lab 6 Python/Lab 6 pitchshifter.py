# This lab assumes you have six touchpads on your instrument
# pads 0 to 3 are the same
# pads 4 and 5 transpose the pitches of pads 0-3

from scamp import *

import comms, utils, init
from pynput import keyboard
import threading, math, random
from setup import *

debug = False # set to True to monitor incoming midi messages
number_sensors = 6

# this block runs once when we start run this script
# instr sends midi to the esp32 to reset the mpr121
instr = s.new_midi_part("esp32", 1)
# here we initialize some pd parameters
for m in init.initial_params:
    comms.send_osc(*m)

# set the data to monitor here - either:
# proximity: how close you are to the sensor without touching it (cc 12-23)
# touch_state: if a sensor is touched (note 0-11)
# touch_cap: sensor capacitance if it is touched (cc 0-11)
# or just leave it blank to turn monitoring off
# see the graph by going to the view menu and toggling plotter
monitor = ""


# handlers for incoming midi messages
# for now we send these signals directly to PD
# also remember, we are storing them in the active_notes and ccs arrays
def handle_note(note, velocity):
    if debug: print('note', note, velocity)
    
    new_note = 0
    note_offset = 0
    
    if note < 4:
        if 4 in active_notes: note_offset +=  7
        if 5 in active_notes: note_offset +=  2
        if velocity > 0: new_note = init.touch_pitch[note]
        else: new_note = init.proximity_pitch[note]
        new_note += note_offset
    
        comms.send_osc("voice", note, "pitch", (new_note+48)/127)
        comms.send_osc("voice", note, "trigger", 1 if velocity > 0 else 0)
        comms.send_osc("stereo-delay", 1,"FEEDBACK", (len(active_notes)/10 + .5)*127)
        
    elif note == 4:
        if velocity > 0: note_offset += 7
        if 5 in active_notes: note_offset +=  2
    elif note == 5:
        if velocity > 0: note_offset += 2
        if 4 in active_notes: note_offset +=  7
        
    if note >= 4:
        for i in active_notes:
            index = int(i)
            if index < 4:
               new_note = init.touch_pitch[index] + note_offset
               comms.send_osc("voice", index, "pitch", (new_note+48)/127)
        
    
def handle_cc(num, val):
    if debug: print('cc', num, val)
    if num < 12:
        comms.send_osc("voice", num,"fm", utils.scale(val,0,127,0,.5,2))
    if num >= 12:
        if val < 5: comms.send_osc("voice", num-12,"vca", 0)
        else:
            comms.send_osc("voice", num-12,"vca", val/127)
            comms.send_osc("voice", num-12,"cutoff", val/90+32)


# main loop
# all we do in the loop is monitor the signals
def mainLoop():
    global index
    
    instr.play_note(60,1,.1) # reset the mpr121
    
    while True:
        monitor_values = []
        for i in range(number_sensors):
            
            #monitor
            if monitor == "proximity": monitor_values.append(ccs[i+12])
            if monitor == "touch_state": monitor_values.append(True if i in active_notes else False)
            if monitor == "touch_cap": monitor_values.append(ccs[i])
            
        if len(monitor_values) > 0: print( monitor_values)
        wait(0.125) #this time is in fractions of a beat, e.g. 1/64 of a beat
    
def run_session():
    s.fork(mainLoop)
    s.wait_forever()


        
comms.handle_cc = handle_cc
comms.handle_note = handle_note
s.register_midi_listener(comms.esp32_midi_port, comms.handle_midi)

threading.Thread(target=run_session).start()



