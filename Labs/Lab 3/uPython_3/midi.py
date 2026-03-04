import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

# 1. Set up MIDI
# We use the first available MIDI output port
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

def sendNote(note,vel):
    print(note,vel)
    if vel > 0:
        midi.send(NoteOn(note,vel)) # Send Middle C
    else:
        midi.send(NoteOff(note, 0))
    
def sendCC(num, val):
    print(num,val)
    midi.send(ControlChange(num, val))
