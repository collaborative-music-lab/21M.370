import board
import time
import analogio
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

buttons = []
pots = []

analog_pins = [
    board.IO1,
    board.IO2,
    board.IO3,
    board.IO4,
    board.IO5,
    board.IO6
]
digital_pins = [
    board.IO7,
    board.IO8,
    board.IO9,
    board.IO10,
    board.IO13,
    board.IO11
]