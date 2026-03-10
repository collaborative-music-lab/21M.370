import board
import busio
import adafruit_mpr121

# Create the I2C bus interface
i2c = busio.I2C(board.IO44, board.IO43)

# Initialize the MPR121 sensor
# Note: The default I2C address is 0x5A
cap = adafruit_mpr121.MPR121(i2c)