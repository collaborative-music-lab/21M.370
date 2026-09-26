import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi # custom 21M.370 modules

loop_timer = 0
interval = 0.1
button_state = 0

while True:
    now = time.monotonic()
    
    if now-loop_timer  > interval:
        loop_timer = now
        print('timer', now)

