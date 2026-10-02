# Arpy

import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi, seq, mapping # custom 21M.370 modules

from data import *

# pins for custom creativitas pcb

mapping.send_mapping()

DEBUG = True 

pot = [
    sensors.Potentiometer(4),
    sensors.Potentiometer(3),
    sensors.Potentiometer(2),
    sensors.Potentiometer(1)
    ]


button = [
    sensors.Button(6),
    sensors.Button(7),
    sensors.Button(8),
    sensors.Button(9)
    ]

# use led for status monitoring
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 1
pixel[0] = (255, 100, 0)

button_timer = 0
clock_timer = 0
bpm = 100
bpm_seconds = 60/bpm/2
index = 0
sensor_timer = 0

button_state = [0,0,0,0]
pot_state = [0,0,0,0]

# chord variables
current_chord = [0,2,4]
scale = [0,2,3,5,7,8,10] # c minor scale
base_octave = 4

# arpeggio variables
button_root = [0,3,4,5]

def degreeToMidi(interval):
    extraOctaves = math.floor( interval / len(scale) )
    interval = interval % len(scale)
    note = scale[interval] + (base_octave + extraOctaves) * 12
    
    return note

print( degreeToMidi(-3))

while True:
    now = time.monotonic()
    
    if now - button_timer > 0.001:
        button_timer = now
        for i in range(4):
            val = button[i].read()
            if val == "pressed":
                if DEBUG: print('button ', i, 'pressed')
                button_state[i] = 1
            elif val == "released":
                button_state[i] = 0
    
    if now  - sensor_timer > 0.010:
        sensor_timer = now
        
        if 1:
            msg = []
            for i in range(4):
                val = pot[i].new()
                msg.append(val)
                if val != False:
                    val = val >> 5 # convert 12 to 7-bit
                    if i == 0: midi.send_message("voice", 0, "cutoff", val)
                    
                    pot_state[i] = val
#                 if DEBUG: print(msg)
    
    if now  - clock_timer > bpm_seconds:
        clock_timer = now
        index += 1
        
        index = index % 16
        current_note = current_chord[index % len(current_chord)]
        note_to_play = current_note
        
        # check which buttons are held
        play_note = False
        for i in range(4):
            if button_state[i] == 1:
                play_note = True
                print(index, "button", i, current_note)
                note_to_play = current_note + button_root[i]
                
        if play_note:
            note_to_play = degreeToMidi( note_to_play)
#             note_to_play += base_octave*12
            print(note_to_play)
            midi.send_message("voice", 0, "pitch", note_to_play)
            midi.send_message("voice", 0, "trigger", 0)
