import board
import time
import analogio
import digitalio
from sensors.mpr121 import MPR121

cap = MPR121()
cap.set_sensitivity(63, 0) # (0-63) and (0-7)

values = [0]*12

while True:
    
    for i in range(12):
        values[i] =   cap.baseline_data(i) - cap.filtered_data(i)
            # print(f"Electrode {i} touched!")
    print( values )
    time.sleep(.1)
    
