"""
Nobby.py
Ian Hattwick
Mar 6, 2025

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
''' euclid variables for kick, snare, hihat '''
kickEuclid = { "name":"kick", "hits": 3, "beats": 8, "rotate": 0, "pattern": [0] * 8 }
snareEuclid = { "name":"snare", "hits": 3, "beats": 8, "rotate": 0, "pattern": [0] * 8 }
hatEuclid = { "name":"hat", "hits": 3, "beats": 8, "rotate": 0, "pattern": [0] * 16 }

curBeat = 0

#SYNTH AND SEQUENCER
synthClock = 0
synthRange = 0
synthProgramEnable = 0
synthNewNote = 0
synthClockDivider = 2

######################
# MAIN MAPPING FUNCTION
######################
#store values of pots and switches
pot = [0,0,0,0]
switch = [0,0,0,0]

def isNew(val, prev, threshold):
    '''check if a value has changed beyond the threshold'''
    if abs(prev-val) > threshold:
        return True
    else: return False

def mapSensor(add, val):
    """
    Main mapping function.
    Modify this function to change sensor mappings.
    """
    global synthNewNote, synthProgramEnable, synthClock

    if MONITOR_SENSORS == 1:
        print(add, val)

    #buttons
    if add == "/sw0":
        switch[0] = val
        if val == 1:
            kickEuclid["rotate"] = (curBeat+1)%kickEuclid["beats"]
    elif add == "/sw1": 
        switch[1] = val
        if val == 1:
            snareEuclid["rotate"] = (curBeat+1)%snareEuclid["beats"]
    elif add == "/sw2": 
        switch[2] = val
        if val == 1:
            hatEuclid["rotate"] = (curBeat+1)%hatEuclid["beats"]
    elif add == "/sw3": 
        switch[3] = val
        
    #pots
    #pots to control drum values
    enableDrumEdit = 1 if switch[3] == 1 else 0
    
    if add == "/pot0":
        """set drum pattern"""
        if isNew(val, pot[0],50):
            pot[0] = val
            val = val/4095
            if enableDrumEdit > 0:
                euclids = [kickEuclid, snareEuclid, hatEuclid]
                for i in range(3):
                    if switch[i] == 1:
                        euclids[i]["hits"] = int( val * (euclids[i]["beats"]))
                        euclids[i]["pattern"] = euclid(euclids[i]["hits"],euclids[i]["beats"],0)

    elif add == "/pot1":
        """set drum tone"""
        if isNew(val, pot[1],100):
            pot[1] = val
            if enableDrumEdit > 0:
                for i in range(3): 
                    if switch[i]> 0:
                        drumTone(i,val)
    
    elif add == "/pot2":
        """either determines sequence index, or stores a value in the sequence"""
        if isNew(val, pot[2],50):
            pot[2] = val
            #enable editing the sequence if button 3 is down
            if enableDrumEdit > 0 and synthProgramEnable == 0:
                synthClock = 0
                synthProgramEnable = 1
            elif not enableDrumEdit and synthProgramEnable == 1:
                synthProgramEnable = 0
            #otherwise set the index of the sequence
            elif synthProgramEnable == 0:
                setSynthRange(val)
                synthNewNote = 1

    elif add == "/pot3":
        '''change drum timbre'''
        if isNew(val, pot[3],10):
            pot[3] = val
            val = val/4095
            sendOSC('bob-filter', 1, 'CUTOFF', (val) * 100 + 2)
            sendOSC('bob-filter', 1, 'FM-/+', (val) * 35 + 60)  
            sendOSC('slope', 1, 'FALL', (1-(val)) * 75 + 1)
            sendOSC('decay', 1, 'D', (1-(val)) * 75 + 1)  

######################
# EUCLIDIAN FUNCTION
######################
def euclid(hits, beats, rotate):
    """Generate a Euclidean rhythm pattern.
    
    Args:
        hits (int): Number of active beats (1s).
        beats (int): Total number of beats (steps).
        rotation (int): Number of steps to rotate the pattern.
    
    Returns:
        list: A list representing the rhythmic pattern.
    """
    pattern = []
    pulses = hits
    beats = beats
    bucket = 0
    rotation = rotate+1

    for i in range(beats):
        bucket += pulses
        if bucket >= beats:
            bucket -= beats
            pattern.append(1)
        else:
            pattern.append(0)
    
    # Apply rotation
    rotated_pattern = pattern[-rotation:] + pattern[:-rotation] if rotation else pattern
    print('euclid pattern', rotated_pattern)
    return rotated_pattern 


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

def drumTone(num,val):
    if switch[num] > 0:
        val = val/4095
        outVal=1

        #turn down drum volume at low tone values
        chText = ["CH1", "CH2", "CH3"]
        if val < 0.1: 
            outVal = val*10
        sendOSC('mixer4',1,chText[num],outVal*127)

        outVal = math.pow(val*0.8+0.2,2)
        if num == 1: outVal = math.pow(val*0.8+0.2,2)
        if num == 2: outVal = math.pow(val*0.9+0.1,2)
        sendOSC("decay", num+2, "D", outVal*127) #module name, instance, parameter name, value
        sendOSC("decay", num+12, "D", math.pow(outVal,2)*127)


def setSynthRange(val):
    global synthRange
    val = math.floor(val/4095 * 15) + 1

    if val != synthRange:
        synthRange = val
        sendOSC('16steps',1,'BEGIN', val)
        sendOSC('16steps',1,'END', val)

######################
# OSC COMMS WITH PD
######################
def define_osc_handlers(dispatcher):
    """
    Registers OSC message handlers.
    Modify this function to add custom OSC behavior.
    """
    def unknown_osc_handler(address, *args):
        """Handles unrecognized OSC messages."""
        print(f"Unrecognized OSC message: {address} {args}")

    dispatcher.map("/cancel", setup.t.cancel)
    dispatcher.map("/clock", clock)
    dispatcher.set_default_handler(unknown_osc_handler) 
    print("OSC handlers registered.")

def clock(*args):
    global eucClock, synthProgramEnable, synthNewNote, synthClock, synthRange, synthClockDivider, prevTime, curBeat
    setup.t.update() #reset timeout
    curBeat = args[2]%16 #clock is just an ascending integer
    
    #drum sequencers
    euclids = [kickEuclid, snareEuclid, hatEuclid]
    for i in range(3):
        if switch[i] == 1:
            pattern = euclids[i]["pattern"]
            index = int(curBeat - euclids[i]["rotate"]) % euclids[i]["beats"]

            if pattern[index] == 1:
                sendOSC("trigger", i*2)
                sendOSC("trigger", (i*2+5)%6)

    #synth
    if curBeat % synthClockDivider == 0: #synth clock is divided by N
        if synthProgramEnable == 1:
            #write the current value of pot 2 into the sequence
            sendOSC("16steps", 1, "s"+str(synthClock+1), math.floor(pot[2]/4095 * 127))
            setSynthRange(synthClock * (4095/16) )
            sendOSC("trigger", 6)
            synthClock += 1
            if synthClock >= 16: synthClock = 0

        elif synthNewNote == 1:
            #otherwise just trigger the note if it has changed
            sendOSC("trigger", 6)
            synthNewNote = 0

#####################
# Start the system, passing in `mapSensor` and `define_osc_handlers`
######################
if __name__ == "__main__":
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)  
    
    try:
        loop.run_until_complete(setup.init_system(mapSensor, define_osc_handlers))
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Shutting down...")
        loop.run_until_complete(setup.shutdown())
    finally:
        loop.close()