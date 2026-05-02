import board
import time
import analogio
import digitalio

# my code from other scripts
import sensors

buttons = []
pots = []

for pin in range(1,5):
    pots.append( sensors.Pot(pin) )

for pin in range(6,10):
    buttons.append( sensors.Button(pin) )

while True:
    value = 0
#     for i, pot in enumerate(pots):
#         value = pot.read()
#         if value is not False:
#             print('pot', i, value)
    for i, button in enumerate(buttons):
        value = button.read()
        if value is not False:
            print('button', i, value)
            velocity = 100 if value == 'pressed' else 0
    time.sleep(.01)
    

