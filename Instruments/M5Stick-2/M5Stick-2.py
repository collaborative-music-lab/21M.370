"""
Chester.py
Ian Hattwick
Apr 4, 2025

Main script handling mappings.
Setup variables for configuring communicaton with ESP32
and OSC are in setup.py
"""
MONITOR_SENSORS = 0
enableIMUmonitoring = 0

import setup  # Import setup module
import asyncio
import math

######################
# GLOBAL VARIABLES
######################
state = {
    #raw data
    'accel': [0,0,0],
    'velocity': [0,0,0], #accel integration
    'jerk': [0,0,0], #accel derivative
    'magnitudeA': 0, #total acceleration
    'magnitudeB': 0, #total acceleration
    'accelTilt': [0,0,0],

    'gyro': [0,0,0],
    'angle': [0,0,0], #gyro integration

    'encoder': 0,
    'photocell':0,

    #buffers for data
    'accelIndex': 0,
    'accelBufferLength': 8,
    'accelBuffer': [0,0,0] * 8,

    'gyroBuffer': [[0,0,0]],
    'gyroIndex': 0,
    'gyroBufferLength': 8,
    'tilt': [0,0,0],

    #cooked data
    #smoothed
    'accelSmooth': [0,0,0], #using onepole
    'magnitudeSmooth': 0,
    'accelAvg': [0,0,0], #average of buffer
    'accelMean': [0,0,0], #mean of buffer
    'accelMin': [0,0,0], #minimum val in buffer
    'accelMax': [0,0,0], #maximum val in buffer
    'gyroSmooth': [0,0,0],
}


tuning = {
    #variables for smoothing filters
    'accelSmooth' : 0.9,
    'magnitudeSmooth': 0.6,
    'magnitudeFade': 0.1,
    'magnitudeGain': 4,
    'tiltSmooth': 0.9,
    'velocitySmooth': 1,
    'photoSmooth': .5,
}

def mapSensor(device, add, val):
    global state, MONITOR_SENSORS
    
    sensor,num = splitAddress(add)
    if MONITOR_SENSORS == 1:# and add not in ['/acc0', '/gyro0']:
        print('MONITOR_SENSORS', device, add, val)

    if device == 'IMH-D4D4':
        if sensor == '/acc':
            mag = calcMagnitude(val)
            state['magnitudeA'] = onepole2(state['magnitudeA'], mag, 0.96)
            setup.client.send_message( "/aX", state['magnitudeA'])
            sendOSC('vca',1,'VCA',state['magnitudeA'] * 127)
            #print('d4',state['magnitudeA'])
            tilt = calcTiltAccel(val)
            sendOSC('vca',1,'CV',tilt[0] * 127)
            sendOSC('analog-filter',1,'FM-/+',tilt[1] * 127)
            sendOSC('bwl-osc',1,'CV',tilt[2] * 127)
            # sendOSC('vca',1,'CV',tilt[0] * 127)
            sendOSC('analog-filter',1,'CUTOFF',tilt[1] * 64+5)
            sendOSC('bwl-osc',1,'WSHAPE',tilt[2] * 127)

            

    if device == 'IMH-B764':
        if sensor == '/acc':
            mag = calcMagnitude(val)
            state['magnitudeB'] = onepole2(state['magnitudeB'], mag, 0.96)
            setup.client.send_message( "/aY", state['magnitudeB'])
            print('b7', state['magnitudeB'])
            tilt = calcTiltAccel(val)
            sendOSC('vca',2,'VCA',state['magnitudeA'] * 127)
            sendOSC('vca',2,'CV',tilt[0] * 127)
            sendOSC('analog-filter',2,'FM-/+',tilt[1] * 127)
            sendOSC('bwl-osc',2,'CV',tilt[2] * 127)
            sendOSC('analog-filter',2,'CUTOFF',tilt[1] * 64+5)
            sendOSC('bwl-osc',2,'WSHAPE',tilt[2] * 127)
#####IMU FUNCTIONS #######  

def calcTiltAccel(vals):
    '''calculates tilt only using a 3-axis accelerometer'''
    outVal = [0] * 3

    for i in range(3):
        if vals[i] == 0:
            vals[i] = 0.00000000001

    outX = math.atan(vals[0]/ math.sqrt( math.pow(vals[1],2) + math.pow(vals[2],2) ))
    outY = math.atan(vals[1]/ math.sqrt( math.pow(vals[0],2) + math.pow(vals[2],2) ))
    outZ = math.atan(vals[2]/ math.sqrt( math.pow(vals[0],2) + math.pow(vals[1],2) ))

    outVal = [outX, outY, outZ]

    # setup.client.send_message("/tiltX", outVal[0])
    # setup.client.send_message("/tiltY", outVal[1])
    # setup.client.send_message("/tiltZ", outVal[2])

    return outVal


def calcAngle(vals):
    angleLeak = 0.99
    outVal = [0] * 3

    for i in range (3): 
        if abs(vals[i]) > 0.05:
            filteredGyro = clipBipolar( vals[i] , 0.0, 1000)
            outVal[i] = state['angle'][i] + (filteredGyro/4 )
            outVal[i] *= angleLeak
        else: outVal[i] = state['angle'][i] * 0.999


    #print(vals[2], outVal[2])

    setup.client.send_message("/tiltX", outVal[0])
    setup.client.send_message("/tiltY", outVal[1])
    setup.client.send_message("/tiltZ", outVal[2])

    return outVal

def calcTilt(vals):
    '''calculate tilt XYZ using a complementary filter'''
    Gweight = 0.95 #weighting for complementary filter

    outAngle = [0] * 3

    #calculate complementary filter
    for i in range(3): 
        outAngle[i] = state['angle'][i] * 1 + state['accelTilt'][i] * (1-Gweight) 

    setup.client.send_message("/tiltX", outAngle[0])
    setup.client.send_message("/tiltY", outAngle[1])
    setup.client.send_message("/tiltZ", outAngle[2])

    return outAngle

def calcMagnitude(vals):
    '''calculate magnitude as the sum of all acceleration vectors'''
    val = math.sqrt( math.pow(vals[0],2) + math.pow(vals[1], 2) + math.pow(vals[2], 2))
    val = abs(val*18-0.6) #remove static acceleration

    #state['magnitude'] = onepole2(state['magnitude'], val, 0.3)
    return val
    # setup.client.send_message( "/magnitude", val)
    #setup.client.send_message( "/magnitude", state['magnitude'])

    #return state['magnitude']

def calcVelocity(vals):
    #integrate acceleration
    velocityLeak = 0.9
    outVal = [0] * 3

    for i in range(3):
        outVal[i] += vals[i]
        outVal[i] *= velocityLeak

    setup.client.send_message("/velocityX", outVal[0])
    setup.client.send_message("/velocityY", outVal[1])
    setup.client.send_message("/velocityZ", outVal[2])
    #print(tuning['velocitySmooth'])

    return outVal

def calcJerk(vals):
    '''derivative of acceleration'''
    outVal = [0]*3
    for i in range(3):
        outVal[i] = vals[i] - state['accel'][i]

    if enableIMUmonitoring == 1:
        setup.client.send_message("/jX", outVal[0])
        setup.client.send_message("/jY", outVal[1])
        setup.client.send_message("/jZ", outVal[2])
    #print(state['jerk'])

    return outVal

def calcSmoothAccel(vals,coefficient):
    '''simple lowpass filter for accel'''
    tuning['accelSmooth']
    outVal = [0] * 3
    for i in range(3):
        outVal[i] = onepole2(vals[i],state['accel'], tuning['accelSmooth'])
    #print(state['aMag'])
    sendRawAccel(vals)

    return outVal

def sendRawAccel(vals):
    if enableIMUmonitoring == 1:
        setup.client.send_message("/aX", vals[0])
        setup.client.send_message("/aY", vals[1])
        setup.client.send_message("/aZ", vals[2])

def sendRawGyro(vals):
    if enableIMUmonitoring == 1:
        setup.client.send_message("/gX", vals[0])
        setup.client.send_message("/gY", vals[1])
        setup.client.send_message("/gZ", vals[2])

def bufferAccel(vals):
    state['accelIndex'] += 1
    if state['accelIndex'] >= state['accelBufferLength']: state['accelIndex'] = 0
    state['accelBuffer'][state['accelIndex']] = vals



# onepole2 implements a simple one-pole lowpass filter
# arguments: previousOutput, newData, filter coefficient
# - previousOutput and newData can be either single values or arrays
def onepole2(old, new, coefficient):
    #convert single values into arrays of length 1
    if isinstance(new, int) is True or isinstance(new, float) is True:
        old = [old]
        new = [new]
    outVal = [0] * len(old)

    clip (coefficient, 0, 1)

    #main filtering stage
    for i in range(len(old)):
        outVal[i] = (new[i]*(1-coefficient) + old[i]*coefficient)

    if len(outVal) == 1:
        return outVal[0]
    return outVal

def leakyInt(bucket, val, leak):
    bucket *= leak 
    bucket += val
    return bucket
######################
#Helper functions
######################
def splitAddress(name):
    for i in range(len(name)):
        if name[i].isdigit():
            return name[:i], int(name[i:])
    return name, None  # If no digits found

def scale(input, inLow, inHigh, outLow, outHigh, curve = 1):
    val = (input-inLow)/(inHigh-inLow)
    val = pow(val,curve)
    val = val*(outHigh-outLow) + outLow
    return val

def sendOSC(module, instance=0, param=None, val=None):
    '''send OSC messages to PD in automitonism format '''
    if param == None: #handle messages with one argument, for PD receive objects
        param = instance
        val = instance
    setup.client.send_message('/module', module)
    msg = [param, val, instance]
    setup.client.send_message('/param', msg)


def clip(input, low, hi):
    if input > hi: return hi
    elif input < low: return low
    else: return input

def clipBipolar(input, low, hi):
    '''filters out small numbers from bipolar variables'''
    sign = 1
    if input<0: sign = -1
    outVal = abs(input)

    if outVal > hi: outVal =  hi
    elif outVal < low: outVal =  low
    
    return (outVal-low) * sign 



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
    dispatcher.set_default_handler(unknown_osc_handler) 
    print("OSC handlers registered.")


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