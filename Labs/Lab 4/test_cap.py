import board
import time
import analogio
import digitalio
from sensors.mpr121 import MPR121

cap = MPR121()

values = [0]*12

while True:
    
    for i in range(12):
        values[i] =   cap.baseline_data(i) - cap.filtered_data(i)
            # print(f"Electrode {i} touched!")
    print( values )
    time.sleep(.1)
    
