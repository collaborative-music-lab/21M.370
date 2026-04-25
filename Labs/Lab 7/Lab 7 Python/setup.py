from scamp import *
import math, random

print_available_midi_input_devices()
esp32_midi_port = 1 #change to the current port for your system

tempo = 60 + random.random()*10
s = Session(tempo)


# dictionary for midi cc messages
ccs = {i: 0 for i in range(128)}

# dictionary for MIDI note messages that are currently ON
# receining a note off msg removes it from this list
active_notes = {}