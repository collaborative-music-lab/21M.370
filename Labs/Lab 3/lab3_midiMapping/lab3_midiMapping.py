# Example script showing to to send midi messages to automatonism

from scamp import *
import comms, setup
from pynput import keyboard
import threading, math
from session import s, tempo

debug = True # set to false to minimize clock lagging

tempo = 96
s.register_midi_listener(comms.esp32_midi_port, comms.handle_midi)

def handle_note(note, velocity):
    if debug: print('note', note, velocity)
    comms.send_osc('newNote', note)
comms.handle_note = handle_note
    
def handle_cc(num, val):
    if debug: print('cc', num, val)
    if num == 0: comms.send_osc('ladder-filter', 1, 'FREQ', val)
comms.handle_cc = handle_cc

def mainLoop():
    # this function will be called repeatedly
    pass

setup.mainLoop = mainLoop
threading.Thread(target=setup.run_session).start()