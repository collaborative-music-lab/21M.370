# Capacit code.py
# try changing the capsense alpha for smoothing, and the sensor_interval for update rate

import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi, seq, mapping # custom 21M.370 modules
from sensors.mpr121 import MPR121

DEBUG = True

mpr = MPR121()
mpr.set_sensitivity(63, 0) # (0-63) and (0-7)

# initial PD parameters
midi.send_param("bwl-osc", 1, "FM", 127)
midi.send_param("ladder-filter", 1, "FM-/+", 127)
midi.send_param("bwl-osc", 1, "WSHAPE", 2)
midi.send_param("stereo-delay", 1, "RATE-LEFT", 60)
midi.send_param("stereo-delay", 1, "RATE-RIGHT", 62)
midi.send_param("maestro4", 1, "CH3", 40)
midi.send_param("maestro4", 1, "CH4", 40)

num_capsense = 4

capsense_timer = 0
clock_timer = 0
sensor_timer = 0
sensor_interval = 0.1 # in seconds

bpm = 100
bpm_seconds = 60/bpm/2
index = 0

melody = [0,2,5,4, 2, 1, 3, 7]
index = [0,0,0,0]
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
        self.raw = 0
        self.alpha = 0.3 # for smoothing
        self.touch = 0
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
        
        if self.raw > self.baseline + self.touch_threshold:
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
    if waiting_to_initialize:
        if now - start_time < 1:
            print("waiting to initialize", now-start_time)
            time.sleep(.1)
            continue
        else: waiting_to_initialize = False
    
    if now - capsense_timer > 0.005:
        capsense_timer = now
        
        mpr.update()
        
        for i in range(num_capsense):
            cap[i].update(mpr.read(i))
            if cap[i].state == "pressed":
                index[i] = (index[i]+1) % len(melody)
                midi.send_message( "voice",i,"pitch",degreeToMidi(melody[index[i]] + i*7))
        
    if now  - sensor_timer > sensor_interval:
        sensor_timer = now
        
        for i in range(num_capsense):
            proximity = cap[i].proximity*127*5
            touch = cap[i].touch*12
            if proximity > 127: proximity = 127
            midi.send_message("voice", i, "vca", proximity)
            midi.send_message("voice", i, "cutoff", proximity*.8)
            midi.send_message("voice", i, "fm", touch)
            
            if DEBUG:  print(i, mpr.read(i), cap[i].proximity, cap[i].touch)
    
    if now  - clock_timer > bpm_seconds:
        clock_timer = now

        total_proximity = sum([cap[i].proximity for i in range(num_capsense)]) / num_capsense        
        midi.send_param("stereo-delay", 1, "FEEDBACK", 100 - total_proximity*80)

