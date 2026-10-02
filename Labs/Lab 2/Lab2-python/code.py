import board, analogio, digitalio # hardware imports
import usb_midi, adafruit_midi, neopixel # adafruit software modules in lib folder
import time, math, random # standard python modules
import sensors, midi # custom 21M.370 modules

loop_timer = 0
interval = 0.1
button_state = 0

pot = [
    sensors.Potentiometer(4), # index 0
    sensors.Potentiometer(3),
    sensors.Potentiometer(2),
    sensors.Potentiometer(1)
    ]

buttons = [
    sensors.Button(6),
    sensors.Button(7),
    sensors.Button(8),
    sensors.Button(9)
    ]

while True:
    now = time.monotonic()
    
    for i in range(4):
        val = buttons[i].read()
        if val == "pressed":
            print(i, "pressed")
        elif val == "released":
            print(i, "released")
    
    if now-loop_timer  > interval:
        loop_timer = now
        val = [0,0,0,0]
        for i in range(4):
            val[i] = pot[i].read()
        print(val)
