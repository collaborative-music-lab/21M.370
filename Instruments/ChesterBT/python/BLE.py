import asyncio
from bleak import BleakScanner, BleakClient

TARGET_NAME = "ESP-4"
TARGET_ADDRESS = "d520d7f2-f52f-1da0-8a76-9fbf7f2d74cb"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def run():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=5.0)

    esp32 = None
    for d in devices:
        print(f"Found device: {d.name}, {d.address.lower()}")
        if d.address.lower() == TARGET_ADDRESS:
            esp32 = d
            break

    if esp32 is None:
        print(f"Could not find device with name '{TARGET_ADDRESS}'")
        return

    async with BleakClient(esp32.address) as client:
        print(f"Connected to {esp32.name}!")

        def notification_handler(sender, data):
            if len(data) <= 64:
                        print(f"Notification: {data}")
            else:
                print(f"Unexpected data length: {len(data)} bytes")
                
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        #print("Connected. You can type commands now (LED_ON, LED_OFF, etc). Ctrl+C to exit.")

        while True:
        #     user_input = input("> Enter command: ")
        #     if user_input.strip():
        #         await client.write_gatt_char(CHARACTERISTIC_UUID, user_input.encode('utf-8'))
             #print('waiting')
             await asyncio.sleep(0.5)

asyncio.run(run())