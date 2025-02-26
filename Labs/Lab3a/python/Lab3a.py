"""
Lab3a.py
Ian Hattwick
Feb 25, 2025

Main script handling mappings.
Setup variables for configuring communicaton with ESP32
and OSC are in setup.py
"""

import setup  # Import setup module
import asyncio

######################
# GLOBAL VARIABLES
######################
euclidHits = 3
euclidBeats = 8
euclidRotate = 0
euclidPattern = []#euclid(euclidHits,euclidBeats,euclidRotate)

######################
# MAIN MAPPING FUNCTION
######################
def mapSensor(add, val):
    """
    Processes sensor data and converts it into an OSC-compatible (address, value) tuple.
    Modify this function to change sensor mappings.
    """
    global euclidHits, euclidBeats, euclidRotate, euclidPattern

    #monitor incoming events - set to False to disable
    if False: 
        print(add, val)

    #buttons
    if add == "/sw0": 
        pass
    elif add == "/sw1": 
        pass
    elif add == "/sw2": 
        pass
    elif add == "/sw3": 
        pass
        
    #pots
    if add == "/pot0":
        hits = int(val/510)
        if hits != euclidHits:
            euclidHits = hits
            euclidPattern = euclid( euclidHits, euclidBeats, euclidRotate)
    elif add == "/pot1":
        pass
    elif add == "/pot2":
        pass
    elif add == "/pot3":
        pass 
 
######################
# EUCLIDIAN FUNCTION
######################
def euclid(pulses=3, beats=8, rotation=0):
    """Generate a Euclidean rhythm pattern.
    
    Args:
        hits (int): Number of active beats (1s).
        beats (int): Total number of beats (steps).
        rotation (int): Number of steps to rotate the pattern.
    
    Returns:
        list: A list representing the rhythmic pattern.
    """
    pattern = []
    bucket = 0
    rotation += 1

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

euclidPattern = euclid(euclidHits,euclidBeats,euclidRotate)

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
    #global eucClock, synthProgramEnable, synthNewNote, synthClock, synthRange, synthClockDivider, prevTime
    setup.t.update() #reset timeout
    print('clock', args[2]) #clock is just an ascending integer
    if euclidPattern[ int(args[2]%euclidBeats) ] == 1:
        sendOSC('trigger', 0)

######################
#Helper functions
######################
def sendOSC(module, instance, param=0, val=0):
    setup.client.send_message('/module', module)
    msg = [param, val, instance]
    setup.client.send_message('/param', msg)

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