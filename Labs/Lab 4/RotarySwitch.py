# Rotary Switch Class

import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi, seq, mapping # custom 21M.370 modules

from data import *

DEBUG = True

class RotarySwitch:
    def __init__(self, pin, num_states = 5):
        self.pot = sensors.Potentiometer(pin)
        self.num_states = num_states
        # more variables here
        self.split_points = self.makeSplitPoints(self.num_states)
        
    def new(self):
        val = self.pot.read()
        # use one-pole lpf to smooth incoming data
        # check new value against prev_value plus schmitt trigger thresholds
        # return false if the value hasn't changed
        # else return (the new state + 1)
        # 0 evaluates to false so we don't want to use state 0
  
        
    def makeSplitPoints(self, num):
        # return an array with the split points for the different states
        
switch = RotarySwitch(1)

# Main code
sensor_timer = 0
sensor_interval = 0.1

while True:
    now = time.monotonic()
    
    if now  - sensor_timer > sensor_interval:
        sensor_timer = now
        
        state = switch.new()
        if state != False:
            print(state)
    