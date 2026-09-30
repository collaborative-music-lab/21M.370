# Nobby

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

euclid = [
    seq.EuclideanSequencer(16),
    seq.EuclideanSequencer(16),
    seq.EuclideanSequencer(16)
    ]

# use led for status monitoring
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 1
pixel[0] = (255, 100, 0)

button_timer = 0
clock_timer = 0
bpm = 100
bpm_seconds = 60/bpm/4
index = 0
sensor_timer = 0

button_state = [0,0,0,0]
pot_state = [0,0,0,0]


counter = 0

while True:
    now = time.monotonic()
    current_time = time.monotonic()
    
    if now - button_timer > 0.001:
        button_timer = now
        for i in range(4):
            val = button[i].read()
            if val == "pressed":
                if DEBUG: print('button ', i, 'pressed')
                button_state[i] = 1
                if i < 3:
    #                 midi.send_event( "trigger", i)
                    euclid[i].set_rotate(index)
                    if DEBUG: print(euclid[i].sequence)
            elif val == "released":
                button_state[i] = 0
    
    if now  - sensor_timer > 0.010:
        sensor_timer = now
        
        if 1:
            msg = []
            for i in range(4):
                val = pot[i].new()
                if val != False:
                    val = val >> 5 # convert 12 to 7-bit
                    if i < 3:
                        euclid[i].set_hits( math.floor(scale(val, 0,127,0,12) ))
                    elif i == 3 and val != pot_state[3]:
                        midi.send_param("ladder-filter", 1, "FREQ", scale(val,0,127,8,90))
                        midi.send_param("slope", 1, "FALL", scale(val, 0,127,80,0))
#                         midi.send_cc(10,val)

                    msg.append(val)
                    pot_state[i] = val
#                 if DEBUG: print(msg)
    
    if now  - clock_timer > bpm_seconds:
        clock_timer = now
#         index += 1
        
        msg = [index]
        
        #check which button are held
        for i in range(4):
            if button_state[i] == 1:
                #for drums
                if i < 3:
                    if euclid[i].get(index) == 1:
                        midi.send_event( "trigger", i)
                else:
                    midi.send_event( "bass", 0)
        index += 1
        
        print(counter)
        counter = 0
    counter = counter + 1

#         midi.send_sysex(0x01, ["basic-osc", 0, 'PITCH', index%127*10+100])
#         midi.send_note((index)%127,127)
    
                    
