from scamp import *
import math, random
from euclideanSequencer import EuclideanSequencer

print_available_midi_input_devices()
esp32_midi_port = 0 #change to the current port for your system

tempo = 120
s = Session(tempo)

piano = s.new_part("piano")

root_notes = {
    0: 60,  #C
    1: 64,  #E
    2: 67,  #G
    3: 71   #B
}

chord_types = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "diminished": [0, 3, 6],
    "augmented": [0, 4, 8],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7]
}

chord_type_list = list(chord_types.keys())

current_chords = {
    0: "major",
    1: "major",
    2: "major",
    3: "major"
}

# dictionary for midi cc messages
ccs = {}

# dictionary for MIDI note messages that are currently ON
# receining a note off msg removes it from this list
active_notes = {}

# our sequencers
euclid = {
    "kick":  EuclideanSequencer(beats=8, hits=4),
    "snare": EuclideanSequencer(beats=16, hits=4),
    "hihat": EuclideanSequencer(beats=16, hits=4),
    "synth":  EuclideanSequencer(beats=16, hits=4)
}
euclid["kick"].make_sequence()

# generate a sequence for the synth
synth_sequence = []
minor_scale = [0,2,3,5,7,8,11,12]
for i in range(16):
    synth_sequence.append( minor_scale[ math.floor( math.sin(i)*7 ) ] )
print( synth_sequence )
