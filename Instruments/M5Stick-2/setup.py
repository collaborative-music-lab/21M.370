import asyncio
import time
from pythonosc import udp_client
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import scripts.timeout as timeout
import sensorInput as sensor

PACKET_INCOMING_SERIAL_MONITOR = 0

SERIAL_RECEIVE_PORT = 5010
OSC_PORT = 5005
OSC_SERVER_PORT = 5006
TIMEOUT_DURATION = 5

# Create a shutdown event
shutdown_event = asyncio.Event()

# Initialize components

t = timeout.Timeout(TIMEOUT_DURATION)
serial = udp_client.SimpleUDPClient("127.0.0.1", SERIAL_RECEIVE_PORT)
client = udp_client.SimpleUDPClient("127.0.0.1", OSC_PORT)
dispatcher = Dispatcher()

print(f"Receiving serial from port {SERIAL_RECEIVE_PORT} on localhost")
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

# Define a Datagram Protocol that pushes received UDP data into a queue.
class UDPQueueProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue):
        self.queue = queue

    def datagram_received(self, data, addr):
        self.queue.put_nowait(data)

async def process_serial(map_sensor_function):
    """
    Instead of reading from a serial port, this coroutine listens on the UDP port for incoming data.
    When a UDP packet arrives, it processes it (by calling sensor.processInput, mapping the sensor,
    and sending an OSC message).
    """
    # Create an asyncio Queue to collect incoming UDP datagrams.
    udp_queue = asyncio.Queue()
    loop = asyncio.get_running_loop()
    
    # Create the UDP endpoint that listens on ("127.0.0.1", SERIAL_RECEIVE_PORT)
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPQueueProtocol(udp_queue),
        local_addr=("127.0.0.1", SERIAL_RECEIVE_PORT)
    )

    try:
        data, addr = await asyncio.wait_for(udp_queue.get(), timeout=0.001)
        # Decode and print the received message.
        print(data,addr)
        #message = data.decode('utf-8', errors='replace')
        #print(f"Debug: Received UDP message from {addr}: {message}")
    except asyncio.TimeoutError:
            print("Debug: No UDP message received within the timeout period.")

    try:
        while not shutdown_event.is_set() and t.check():
            try:
                current_message = udp_queue.get_nowait()
            except asyncio.QueueEmpty:
                current_message = None

            if current_message:
                if PACKET_INCOMING_SERIAL_MONITOR == 0:
                    if 2 < len(current_message) < 128:
                        device, address, value = sensor.processInput(current_message)
                        map_sensor_function(device, address, value)
                        #client.send_message(address, value)
                else:
                    print("Packet:", current_message)

            # Yield control only if idle
            await asyncio.sleep(0)  # yields control, doesn't delay

    except asyncio.CancelledError:
        print("UDP processing stopped.")
    finally:
        transport.close()


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