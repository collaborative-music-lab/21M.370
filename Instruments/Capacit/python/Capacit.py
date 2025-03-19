"""
Capacit.py
Ian Hattwick
Mar 12, 2025

Main script handling mappings.
Setup variables for configuring communicaton with ESP32
and OSC are in setup.py
"""
MONITOR_SENSORS = 0

import setup  # Import setup module
import asyncio
import math

######################
# GLOBAL VARIABLES
######################

######################
# MAIN MAPPING FUNCTION
######################
#store values of pots and switches
pot = [0,0,0,0]
switch = [0,0,0,0]

prevNoteTrigger = [0]*12
curAmplitude = [0]*12

maxCapValues = [100]*12
isTouched = [0]*12
isProximity = [0]*12


def mapSensor(add, val):
    global maxCapValues

    if MONITOR_SENSORS == 1:
        print(add, val)

    capTouchThreshold = [0.2,0.5]
    capProximityThreshold = [0.05,0.01]

    sensor,num = splitAddress(add)

    if sensor == "/pot":
        pass

    elif sensor == "/sw":
        pass

    if sensor == "/cap" and num <= 6:
        autoScaleCap(num, val)  # Calibrate
        scaledVal = val / maxCapValues[num]  # Ensure properly scaled value
        
        # --- TOUCH Detection ---
        isTouched[num] = schmittTrigger(scaledVal, isTouched[num], capTouchThreshold[1], capTouchThreshold[0])
        
        if isTouched[num]:
            # touch amplitude control
            out = (scaledVal - capTouchThreshold[1]) * 127
            curAmplitude[num] += out
            sendOSC("vca", num+1, "CV", out)
        else: 
            sendOSC("vca", num+1, "CV", 0)

        if isTouched[num]:
            # touch FM amount
            out_fm = (scaledVal - capTouchThreshold[1]) * 127
            if out_fm > 10:
                sendOSC("vca", num+11, "CV", out_fm)
                sendOSC("vca", num+11, "VCA", scale(out_fm, 10, 127, 0, 127))
            else:
                # Proximity FM fallback
                out_prox_fm = clip(scaledVal * 10 - capProximityThreshold[1], 0, 0.2) * 127
                sendOSC("vca", num+11, "CV", out_prox_fm)
                sendOSC("vca", num+11, "VCA", 0)
        else:
            out_prox_fm = clip(scaledVal * 10 - capProximityThreshold[1], 0, 0.2) * 127
            sendOSC("vca", num+11, "CV", out_prox_fm)
            sendOSC("vca", num+11, "VCA", 0)


        # --- PROXIMITY Detection ---
        isProximity[num] = schmittTrigger(scaledVal * 10, isProximity[num], capProximityThreshold[1], capProximityThreshold[0])
        if isProximity[num]:
            # Handle Proximity Behavior
            out_prox = clip(scaledVal * 10 - capProximityThreshold[1], 0, 0.5) * 127
            curAmplitude[num] += out_prox
            sendOSC("vca", num+1, "VCA", out_prox)

            
        else:
            sendOSC("vca", num+1, "VCA", 0)

        # Monitor signal
        outAmp = clip(curAmplitude[num] / 4, 0, 127)
        sendOSC("monitor" + str(num + 1), outAmp, outAmp, outAmp)
        curAmplitude[num] *= 0.75

        # Trigger new note if amplitude falls to low value
        if curAmplitude[num] <= 1:
            if prevNoteTrigger[num] == 0:
                sendOSC("triggerNote", num)
                print("trig", num)
                prevNoteTrigger[num] = 1
        elif curAmplitude[num] > 60:
            prevNoteTrigger[num] = 0

def autoScaleCap(num,val):
    global maxCapValues
    maxCapValues[num] = maxCapValues[num] * 0.999
    if val > maxCapValues[num]: maxCapValues[num] = val

######################
#Helper functions
######################
def sendOSC(module, instance=0, param=None, val=None):
    '''send OSC messages to PD in automitonism format '''
    if param == None: #handle messages with one argument, for PD receive objects
        param = instance
        val = instance
    setup.client.send_message('/module', module)
    msg = [param, val, instance]
    setup.client.send_message('/param', msg)

def scale(input, inLow, inHigh, outLow, outHigh, curve = 1):
    val = (input-inLow)/(inHigh-inLow)
    val = pow(val,curve)
    val = val*(outHigh-outLow) + outLow
    return val

def splitAddress(name):
    for i in range(len(name)):
        if name[i].isdigit():
            return name[:i], int(name[i:])
    return name, None  # If no digits found

def clip(input, low, hi):
    if input > hi: return hi
    elif input < low: return low
    else: return input

def schmittTrigger(value, state, onThreshold, offThreshold):
    """Hysteresis threshold switching for binary state."""
    if state:  # Currently ON
        if value < offThreshold:
            return 0  # Turn off
        else:
            return 1  # Stay on
    else:  # Currently OFF
        if value > onThreshold:
            return 1  # Turn on
        else:
            return 0  # Stay off

######################
# OSC COMMS WITH PD
######################
def defineOscHandlers(dispatcher):
    def unknown_osc_handler(address, *args):
        """Handles unrecognized OSC messages."""
        print(f"Unrecognized OSC message: {address} {args}")

    dispatcher.map("/filterFrequency", filterFrequency)
    dispatcher.map("/pitchRange", pitchRange)
    dispatcher.map("/starlight", starlight)
    dispatcher.map("/FMDepth", FMDepth)
    dispatcher.map("/envelope-s", setEnvelope)
    dispatcher.set_default_handler(unknown_osc_handler) 

def filterFrequency(add, val):
    sendOSC("bob-filter", 1, "CUTOFF", scale(val, 0,127,3,20))
    sendOSC("bob-filter", 2, "CUTOFF", scale(val, 0,127,32,110))
    sendOSC("bob-filter", 3, "CUTOFF", scale(val, 0,127,5,40))
    sendOSC("bob-filter", 4, "CUTOFF", scale(val, 0,127,40,127))

def pitchRange(add,val):
    sendOSC("vca", 21, "VCA", scale(val, 0,127,20, 127))
    sendOSC("vca", 22, "VCA", scale(val, 0,127,0, 60))
    sendOSC("vca", 23, "VCA", scale(val, 0,127,0, 60))
    sendOSC("vca", 24, "VCA", scale(val, 0,127,0, 90))

def starlight(add,val):
    sendOSC("vca", 5, "VCA", scale(val, 0,127,0,100))

def FMDepth(add,val):
    sendOSC("bwl-osc", 1, "FM", scale(val, 0,127,0, 75))
    sendOSC("bwl-osc", 2, "FM", scale(val, 0,127,0, 75))
    sendOSC("bwl-osc", 3, "FM", scale(val, 0,127,0, 75))
    sendOSC("bwl-osc", 4, "FM", scale(val, 0,127,0, 75))

def setEnvelope(add,val):
    sendOSC("slope", 1, "RISE", scale(val, 0,127,127,0))
    sendOSC("slope", 1, "FALL", scale(val, 0,127,127,40))
    sendOSC("slope", 2, "RISE", scale(val, 0,127,127,0))
    sendOSC("slope", 2, "FALL", scale(val, 0,127,127,40))
    sendOSC("slope", 3, "RISE", scale(val, 0,127,127,0))
    sendOSC("slope", 3, "FALL", scale(val, 0,127,127,40))
    sendOSC("slope", 4, "RISE", scale(val, 0,127,127,0))
    sendOSC("slope", 4, "FALL", scale(val, 0,127,127,40))

def initSynthParams():
    pass

#####################
# Start the system, passing in `mapSensor` and `defineOscHandlersç`
######################
if __name__ == "__main__":
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)  
    
    try:
        loop.run_until_complete(setup.init_system(mapSensor, defineOscHandlers))
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Shutting down...")
        loop.run_until_complete(setup.shutdown())
    finally:
        loop.close()