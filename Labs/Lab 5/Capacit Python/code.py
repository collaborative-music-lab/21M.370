# Capacit code.py
# try changing the capsense alpha for smoothing, and the sensor_interval for update rate

import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi, seq, mapping # custom 21M.370 modules
from sensors.mpr121 import MPR121

DEBUG = False

mpr = MPR121()
mpr.set_sensitivity(63, 0)

num_capsense = 4
cap_is_active = [0 for i in range(num_capsense)]
new_chord = [0 for i in range(num_capsense)]

capsense_timer = 0
clock_timer = 0
sensor_timer = 0
sensor_interval = 0.1 # in seconds

bpm = 100
bpm_seconds = 60/bpm/2
index = 0

chords = [
    [0,2,4,8],
    [1,3,5,9],
    [-1,4,7,6],
    [-3,1,6,5]
    ]

melody = [0,2,5,4, 2, 1, 3, 7]
index = [0,0,0,0]
current_chord = 0
base_octave = 2
scale = [0,2,3,5,7,8,10]

# send in a scale degree and return the midi value 
def degreeToMidi(interval):
    extraOctaves = math.floor( interval / len(scale) )
    interval = interval % len(scale)
    note = scale[interval] + (base_octave + extraOctaves) * 12
    
    return note

class CapSense:
    # keeps track of state and values for one pad
    def __init__(self):
        self.touch = 0
        self.raw = 0
        self.alpha = 0.3 # for smoothing
        self.proximity = 0
        self.proximity_threshold = 10
        self.touch_threshold = 200
        self.baseline = 0
        self.max_value = 800
        self.state = "up"
        
    def update(self, val):
        if val < self.baseline: self.baseline = val
        elif val < self.touch_threshold: self.baseline = self.baseline + 0.1
        
        # onepole filter for raw value
        self.raw = val*(1-self.alpha) + self.raw * self.alpha
        
        if val > self.baseline + self.touch_threshold:
            self.touch = (self.raw - self.touch_threshold) / self.max_value
            self.proximity = 1
            if self.state == "up": self.state = "pressed"
            else: self.state = "down"
        elif self.raw > self.proximity_threshold:
            self.proximity = (self.raw-self.proximity_threshold) / (self.touch_threshold-self.proximity_threshold)
            self.touch = 0
            if self.state == "down": self.state = "released"
            else: self.state = "up"
        else:
            self.touch = 0
            self.proximity = 0

cap = [CapSense() for i in range(num_capsense)]

waiting_to_initialize = True
start_time = time.monotonic()
while True:
    now = time.monotonic()
    if now - start_time < 1:
        print("waiting to initialize", now-start_time)
        time.sleep(.1)
        continue
    
    if now - capsense_timer > 0.005:
        capsense_timer = now
        
        mpr.update()
        
        for i in range(num_capsense):
            cap[i].update(mpr.read(i))
            if DEBUG:  print(i, mpr.read(i), cap[i].proximity, cap[i].touch, cap_is_active, new_chord)
            if cap[i].state == "pressed":
                index[i] = (index[i]+1) % len(melody)
                midi.send_message( "voice",i,"pitch",degreeToMidi(melody[index[i]] + i*7))
#                 if new_chord[i] > 0:
#                     new_chord[i] = 0
#                     interval = chords[current_chord][i] + i*7
#                     midi.send_message( "voice",i,"pitch",degreeToMidi(interval))
#                     print("pitch", i, degreeToMidi(interval))
        
    if now  - sensor_timer > sensor_interval:
        sensor_timer = now
        
        for i in range(num_capsense):
            proximity = cap[i].proximity*127*5
            if proximity > 127: proximity = 127
            midi.send_message("voice", i, "vca", proximity)
            midi.send_message("voice", i, "cutoff", proximity*.8)
            midi.send_message("voice", i, "fm", cap[i].touch*127)
            
            if cap[i].proximity > 0: cap_is_active[i] = 1
            else: cap_is_active[i] = 0

    
    if now  - clock_timer > bpm_seconds:
        clock_timer = now
#         index += 1
        print( "active:", cap_is_active, "     waiting for new note:", new_chord)
        total_proximity = sum([cap[i].proximity for i in range(num_capsense)]) / num_capsense
        
        midi.send_param("stereo-delay", 1, "FEEDBACK", 80 - total_proximity*80)
        
        if sum(cap_is_active) == 0 and sum(new_chord) == 0:
            current_chord = (current_chord+1) % len(chords)
            new_chord = [1 for i in range(num_capsense)]
            print("new chord", current_chord, chords[current_chord])
             