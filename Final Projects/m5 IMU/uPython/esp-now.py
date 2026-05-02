import espnow
import wifi
import struct

# 1. Initialize WiFi
wifi.radio.enabled = True
wifi.radio.start_ap("Sniffer", "12345678", channel=6)
wifi.radio.stop_ap()

# Use a distinct name for the radio object
esp = espnow.ESPNow()

MSG_FORMAT = "<4s3f3fB"
# Hardcoded to match your 29-byte packet
EXPECTED_SIZE = 29 

print("Listening for IMU packets...")

accel = [0,0,0]
gyro = [0,0,0]

def update:
    # Check if there are any packets waiting in the buffer
    if len(esp) > 0:
        packet = esp.read()
        
        # Double-check that packet is not None and has the msg attribute
        if packet is not None:
            try:
                # Now it is safe to access packet.msg
                raw_msg = packet.msg
                
                if len(raw_msg) == EXPECTED_SIZE:
                    data = struct.unpack(MSG_FORMAT, raw_msg)
                    # Check header bytes
                header = data[0].decode().strip('\x00')
                if header == "imu":
                    accel = data[1:4]
                    gyro = data[4:7]
                    extra = data[7]
                    
                    print(f"--- IMU [Extra: {extra}] ---")
                    print(f"Accel: {accel[0]:>6.2f} {accel[1]:>6.2f} {accel[2]:>6.2f}")
                    print(f"Gyro:  {gyro[0]:>6.2f} {gyro[1]:>6.2f} {gyro[2]:>6.2f}")
                else:
                    print(f"Skipping packet: expected {EXPECTED_SIZE} bytes, got {len(raw_msg)}")
            
            except Exception as err:
                print(f"Processing error: {err}")
