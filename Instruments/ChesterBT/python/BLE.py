import asyncio
from bleak import BleakScanner, BleakClient
import socket
import sys

# ------------------ Configuration ------------------
UDP_IP = "127.0.0.1"
UDP_PORT = 5010

DEFAULT_TARGETS = ["ESP32", "d520d7f2-f52f-1da0-8a76-9fbf7f2d74cb"]
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# ------------------ UDP Socket ------------------
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ------------------ SLIP Decoder ------------------
class SlipDecoder:
    def __init__(self, name):
        self.inputBuffer = []
        self.packetList = []
        self.escFlag = False
        self.name = name
        self.total_packets = 0
        self.notification_count = 0
        self.last_packet = None

    def feed(self, data):
        END_BYTE = 255
        ESC_BYTE = 254
        self.notification_count += 1

        for val in data:
            if self.escFlag:
                self.inputBuffer.append(val)
                self.escFlag = False
            elif val == ESC_BYTE:
                self.escFlag = True
            elif val == END_BYTE:
                packet =  bytes(self.inputBuffer)
                self.packetList.append(packet)
                self.last_packet = packet
                self.inputBuffer = []
                self.total_packets += 1
                #print(list( packet))    
            else:
                self.inputBuffer.append(val)

        # Print every 1000 notifications
        if self.notification_count % 1000 == 0:
            print(f"[{self.name}] {self.notification_count} notifications, "
                  f"{self.total_packets} packets, last: {list(self.last_packet) if self.last_packet else 'N/A'}")


    def send(self):
        while self.packetList:
            packet = self.packetList.pop(0)
            #if packet[0] == 0:
                    #print('but 0')
            named_packet = self.name.encode('utf-8') + b':' + packet
            udp_socket.sendto(named_packet, (UDP_IP, UDP_PORT))
            #print(f"[{self.name}] Sent: {list(named_packet)}")

# ------------------ BLE Connection Manager ------------------
async def connect_device(device):
    decoder = SlipDecoder(device.name or device.address)
    client = BleakClient(device)

    async def notification_handler(sender, data):
        decoder.feed(bytearray(data))
        decoder.send()

    try:
        await client.connect()
        print(f"Connected to {device.name} ({device.address})")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        while True:
            await asyncio.sleep(0.01)
    except Exception as e:
        print(f"[{device.name}] Error: {e}")
    finally:
        await client.disconnect()

# ------------------ Main Routine ------------------
async def run():
    user_targets = sys.argv[1:]
    targets = user_targets if user_targets else DEFAULT_TARGETS
    targets = [t.lower() for t in targets]

    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=2.0)

    for d in devices:
        print(f"Found device: {d.name}, {d.address.lower()}")

    matching_devices = [
        d for d in devices if (d.name and d.name.lower() in targets) or (d.address.lower() in targets)
    ]

    if not matching_devices:
        print("No matching BLE devices found.")
        return

    print(f"Connecting to {len(matching_devices)} device(s)...")

    await asyncio.gather(*(connect_device(d) for d in matching_devices))

# ------------------ Entry Point ------------------
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nStopped by user.")