import board
import time
import analogio
import digitalio

# my code from other scripts
import sensors, midi

buttons = []
pots = []
notes = [60,62,64,65]

pins = [getattr(board, f"IO{i}") for i in range(1, 11)]

# analog on pins 0-5
for pin in range(6):
    pots.append( sensors.Pot( pins[pin] ))
    
# digital for pins 6-9
for pin in range(6,9):
    buttons.append( sensors.Button( pins[pin] ))

while True:
#     readButtons()
    value = 0
    for i in [0]:
        value = pots[i].read()
        if value is not False:
            print('pot', i, value)
            midi.sendCC(i, value)
    for i in [0,1,2]:
        value = buttons[i].read()
        if value is not False:
            print('button', i, value)
            velocity = 100 if value == 'pressed' else 0
            midi.sendNote(notes[i], velocity)
#     sendMidi()
    time.sleep(.1)
    
