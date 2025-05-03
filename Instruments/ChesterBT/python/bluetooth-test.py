import serial
import time
from serial.tools import list_ports

ports = list(list_ports.comports())
print("Available ports:")
for p in ports:
    print(p.device, p.description)

serial_port = '/dev/cu.ChesterBT'

ser = serial.Serial(serial_port, 460800, timeout=0.1)

print("Opened port:", serial_port)

try:
    while True:
        if ser.in_waiting > 0:
            val = int.from_bytes(ser.read(), "big")
            print(val)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()