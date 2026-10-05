# Arpy

import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi, seq, mapping # custom 21M.370 modules

from data import *

mapping.send_mapping()

DEBUG = True
bpm = 90
# musical_scale = [0,2,3,5,7,8,10] # c minor scale
musical_scale = [0,2,4,5,7,9,11] # c major scale
phrase_length = 6
transpose = 7 # to set the overall key

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
bpm_seconds = 60/bpm/4
index = 0
sensor_timer = 0

button_state = [0,0,0,0]
pot_state = [0,0,0,0]

# chord variables
current_chord = [0,2,4]
base_octave = 4

# arpeggio variables
button_root = [0,3,4,5]
chord_size = 3 # number of notes in chord
chord_voicing = 0 # lowest note of chord
arp_direction = "up"
newest_button = 0

def degreeToMidi(interval):
    extraOctaves = math.floor( interval / len(musical_scale) )
    interval = interval % len(musical_scale)
    note = musical_scale[interval] + (base_octave + extraOctaves) * 12
    
    return note

def getDegree(degree, chord):
    # gets the current chord degree given the chord_voicing and number of notes
    transpose = math.floor( (degree) / len(chord) )
    degree = degree % len(chord)
    note = chord[degree] + transpose * 14
    
    return note

def makeChord(root):
    global current_chord, arp_direction
    current_chord = []
    base_chord = [0,2,4,7,9,11]
    if chord_size > 64: # jazzier voicing for second half of knob
        base_chord = [0,2,4,6,8,9]
        
    # chord_size is bidirectional, in the center is a small arp and +/- increases and changes arp direction
    arp_direction = "up" if chord_size >= 64 else "down"
    num_notes = abs((chord_size-64) // 6) + 1
    for i in range(num_notes):
        current_chord.append( getDegree( i + chord_voicing, base_chord))
#     print(current_chord, chord_voicing, num_notes)

while True:
    now = time.monotonic()
    
    if now - button_timer > 0.001:
        button_timer = now
        for i in range(4):
            val = button[i].read()
            if val == "pressed":
                if DEBUG: print('button ', i, 'pressed')
                button_state[i] = 1
                newest_button = i
            elif val == "released":
                button_state[i] = 0
    
    if now  - sensor_timer > 0.010:
        sensor_timer = now
        
        if 1:
            msg = []
            for i in range(4):
                
                
                val = pot[i].new()
#                 alpha = 0.5
#                 new_val =  (1-alpha)*val + alpha*pot_state[i]
#                 pot_state[i] = new_val
# #                 if val == False:s break
#                 new_val = scale(new_val, 0, 3900, 0, 127, 2)
#                 if new_val> 127: new_val = 127
#                 print(math.floor(new_val))
#                 break
#                 msg.append(val)
                if val != False:
                    val = val >> 5 # convert 12 to 7-bit
                    if i == 0:
                        chord_size = val
                        makeChord(button_root[i])
                    elif i == 1:
                        chord_voicing = (val//8) - 8
                        makeChord(button_root[i])
                    elif i == 2:
                        midi.send_message("voice", 0, "cutoff", scale(val, 0, 127, 9, 127))
                        midi.send_param("bob-filter", 1, "FM-/+", 90)
                        midi.send_param("slope", 1, "FALL", scale(val, 0, 127, 127, 40))
                    elif i == 3:
                        notes = [-3,-2,-1,1,2] # available roots for button 3
                        button_root[3] = notes[val // 26] # (val // 26) is the same as math.floor(val/32)
                    
                    pot_state[i] = val
#                 if DEBUG: print(msg)
    
    if now  - clock_timer > bpm_seconds:
        clock_timer = now
        index += 1
        num_buttons_held = sum(button_state)
        
        cur_index = index # set the total number of beats per phrase
        
        if num_buttons_held == 0:
            continue
        
        elif num_buttons_held == 1:
            if cur_index % 2 > 0: continue
            cur_index = cur_index//2
        else:
            cur_index = cur_index
            
        cur_index = cur_index % phrase_length # set the total number of beats per phrase
        
        if arp_direction == "down": cur_index = phrase_length-cur_index-1
        
        current_note = current_chord[cur_index % len(current_chord)]
        
        print(cur_index, arp_direction, current_note, current_chord)
#         print(current_chord)
        note_to_play = current_note
        
        # check which buttons are held
        play_note = False
        if button_state[newest_button] == 1:
            play_note = True
            note_to_play = current_note + button_root[newest_button]
                
        if play_note:
            note_to_play = degreeToMidi( note_to_play)
            note_to_play += transpose # changing the key
#             note_to_play += base_octave*12
            # print(note_to_play)
            midi.send_message("voice", 0, "pitch", note_to_play)
            midi.send_message("voice", 0, "trigger", 0)






[ 10, 11, 10, 8, 27,10,9,12]
