"""
######################################################################
# 21M.370 Lab2.py
#
# Description:
# This script sets up an OSC (Open Sound Control) server and client 
# using Python's `python-osc` library. It listens for incoming OSC 
# messages and responds by sending OSC data to a specified address.
#
# The script operates as follows:
# - It initializes an OSC UDP client that sends messages to `127.0.0.1:5005`.
# - It also runs an OSC UDP server listening on `127.0.0.1:5006`.
# - When an OSC message is received, it triggers different functions 
#   based on the message address:
#   - "/getSequence" → Sends a predefined sequence of values.
#   - "/paramName" → Mirrors the received OSC message back.
#   - "/cancel" → terminates the script.
# - If no OSC message is received for 5 minutes, the script will 
#   automatically terminate to prevent infinite execution.
#
# Dependencies:
# - Install required modules with: `pip install python-osc`

######################################################################
"""

import socket
import sys
import asyncio
import time
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher

######################
# TIMEOUT CLASS
######################
class Timeout:
    """Handles automatic script cancellation if no OSC messages are received."""
    
    def __init__(self, interval_minutes=5):
        """Initialize the timeout period in minutes."""
        self._interval = interval_minutes
        self._unit = 60  # Timeout in seconds (interval * unit)
        self._last_update = time.perf_counter()

    def check(self):
        """Checks if timeout has elapsed."""
        return (time.perf_counter() - self._last_update) < (self._interval * self._unit)

    def update(self):
        """Reset the timeout counter."""
        self._last_update = time.perf_counter()

    def cancel(self):
        """Cancel timeout (not used in this version)."""
        self._last_update = 0


# Initialize timeout mechanism
timeout = Timeout(5)

######################
# SETUP OSC
######################
# Initialize UDP client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

# Dispatcher handles OSC messages
dispatcher = Dispatcher()
print("Sending data to port 5005")

# Sequences of scale degrees
SEQUENCES = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [2, 0, 3, 1, 4, 2, 5, 3],
    [0, 4, 7, 11, 14, 18, 14, 7],
    [0, 2, 4, 7, 1, 3, 5, 8],
]

DECAY_TIMES = [20, 50, 90, 127]
TEXT_NUMBERS = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT']


def send_osc(module, instance, param, val):
    """Send OSC messages to specified module."""
    client.send_message('/module', module)
    msg = [param, val, instance]
    client.send_message('/param', msg)


def get_sequence(address, num):
    """Handles OSC message requesting a sequence."""
    timeout.update()  # Reset timeout 

    try:
        num = int(num)
    except ValueError:
        print("Invalid sequence number:", num)
        return

    if 0 <= num < len(SEQUENCES):
        sequence = SEQUENCES[num]
    else:
        print("Sequence number out of range")
        return

    for i, value in enumerate(sequence):
        scaled_value = (value / 27) * 127  # Normalization
        send_osc('8steps', 1, TEXT_NUMBERS[i], scaled_value)
        print(f"Sent: '8steps' {TEXT_NUMBERS[i]} {scaled_value} 1")

    send_osc('slope', 2, 'DEPTH+/-', DECAY_TIMES[num])

timeIncrement = 0
def gen_sequence(address, val):
    """Generate a new sequence in response to an OSC message."""
    timeout.update()  # Reset timeout 


    for i, value in enumerate(sequence):
        scaled_value = random()*32 + val # Normalization
        send_osc('8steps', 1, TEXT_NUMBERS[i], scaled_value)
        send_osc('8steps', 2, TEXT_NUMBERS[i], scaled_value)
        print(f"Sent: '8steps' {TEXT_NUMBERS[i]} {scaled_value} 1")


def mirror(address, val):
    """Passes received OSC message back to the client."""
    timeout.update()  # Reset timeout 
    print(f"Mirroring {address}: {val}")
    client.send_message(address, val)

def cancel_script(val):
    """Cancels the script timeout."""
    timeout.cancel()


# Mapping OSC addresses to functions
dispatcher.map("/getSequence", get_sequence)
dispatcher.map("/genSequence", gen_sequence)
dispatcher.map("/paramName", mirror)
dispatcher.map("/cancel", cancel_script)

from math import floor

def quantize(degree, scale=[0,2,4,5,7,9,11], base_note=60):
    octave = floor(degree / len(scale))
    midiNote = scale[degree % len(scale)]
    return midiNote + octave * 12 + (base_note - 60)

    

async def loop():
    """Main loop to keep script running and check for timeout."""
    while timeout.check():
        await asyncio.sleep(0.001)


async def init_main():
    """Initialize the OSC server and run the main loop."""
    server = AsyncIOOSCUDPServer(("127.0.0.1", 5006), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    try:
        await loop()
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(init_main())