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
                if val != False:
                    val = val >> 5 # convert 12 to 7-bit

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
                print(index, "button", i)
        index += 1


#         midi.send_sysex(0x01, ["basic-osc", 0, 'PITCH', index%127*10+100])
#         midi.send_note((index)%127,127)
    
                    
