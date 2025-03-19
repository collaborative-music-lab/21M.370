import serial
import asyncio
import time
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import scripts.m370_communication as m370_communication
import scripts.timeout as timeout

import sensorInput as sensor

PACKET_INCOMING_SERIAL_MONITOR = 0

# Configurable parameters
SERIAL_ENABLE = True
OSC_PORT = 5005
OSC_SERVER_PORT = 5006
ESP32_DEFAULT_PORT = "/dev/cu.SLAB_USBtoUART"
BAUDRATE = 460800
TIMEOUT_DURATION = 5

# Create a shutdown event
shutdown_event = asyncio.Event()

# Initialize components
comms = m370_communication.communication("serial", baudrate=BAUDRATE, defaultport=ESP32_DEFAULT_PORT)
t = timeout.Timeout(TIMEOUT_DURATION)
client = udp_client.SimpleUDPClient("127.0.0.1", OSC_PORT)
dispatcher = Dispatcher()

print(f"Sending OSC to port {OSC_PORT} on localhost")

# Default timeout handlers
def update_timeout(*args):
    t.update()

def cancel_script(*args):
    t.cancel()

def unknown_osc(*args):
    print("Unknown OSC message received:", args)

dispatcher.map("/tick", update_timeout)
dispatcher.map("/cancel", cancel_script)
dispatcher.set_default_handler(unknown_osc)

async def start_osc_server():
    """Starts the OSC UDP server and returns transport for cleanup."""
    server = AsyncIOOSCUDPServer(("127.0.0.1", OSC_SERVER_PORT), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    return transport

async def process_serial(map_sensor_function):
    """Handles serial data and calls `mapSensor`."""
    try:
        while not shutdown_event.is_set() and t.check():  # Exit if shutdown event is set
        #while not shutdown_event.is_set():  # Exit if shutdown event is set
            await asyncio.sleep(0)
            #print('while', comms.available())
            if SERIAL_ENABLE and comms.available() > 0:
                current_message = comms.get()
                if current_message:
                    if PACKET_INCOMING_SERIAL_MONITOR == 0:
                        if 2 < len(current_message) < 16:
                            address, value = sensor.processInput(current_message)  # Fix variable name
                            map_sensor_function(address, value)
                            client.send_message(address, value)
                    else:
                        print("Packet:", current_message)

            await asyncio.sleep(0.001)
    except asyncio.CancelledError:
        print("Serial processing stopped.")

async def init_system(map_sensor_function, define_osc_handlers_function):
    """Starts OSC server, sensor processing, and handles shutdown with Ctrl+C."""
    define_osc_handlers_function(dispatcher)
    transport = await start_osc_server()

    try:
        print("Setup complete. Running main loop. Press Ctrl+C to quit.")
        client.send_message("/init", 0)
        await process_serial(map_sensor_function)
    except asyncio.CancelledError:
        print("\nShutting down system...")
    finally:
        shutdown_event.set()  # Signal all loops to stop
        transport.close()
        print("Cleanup complete.")

async def shutdown():
    """Triggers shutdown event and cancels all tasks immediately."""
    print("Received shutdown signal. Stopping...")
    shutdown_event.set()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)