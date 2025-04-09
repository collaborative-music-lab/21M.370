import serial
import socket
import sys
from serial.tools import list_ports

# Configuration:
BAUD_RATE = 112500          # Set the baud rate as needed.
UDP_IP = '127.0.0.1'      # Destination IP address for UDP data.
UDP_PORT = 8005           # Destination UDP port.
SELECTED_PORT_INDEX = 4   # Global index for choosing the serial port (change as needed).

def get_serial_port():
    # Retrieve all available serial ports.
    ports = list_ports.comports()
    available_ports = [port.device for port in ports]

    if not available_ports:
        print("No serial ports found.")
        sys.exit(1)

    # Display available ports.
    print("Available serial ports:")
    for idx, port in enumerate(available_ports):
        print(f"{idx}: {port}")

    # Ensure the selected index is within range.
    if SELECTED_PORT_INDEX < 0 or SELECTED_PORT_INDEX >= len(available_ports):
        print(f"Invalid port index: {SELECTED_PORT_INDEX}. Please check the available ports.")
        sys.exit(1)

    selected_port = available_ports[SELECTED_PORT_INDEX]
    print(f"Selected serial port: {selected_port} (index {SELECTED_PORT_INDEX})")
    return selected_port

def main():
    # Use the global index to select a serial port.
    serial_port = get_serial_port()
    
    # Create the UDP socket.
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Open the chosen serial port.
        ser = serial.Serial(serial_port, BAUD_RATE, timeout=1)
        print(f"Opened serial port {serial_port} at {BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Error opening serial port {serial_port}: {e}")
        sys.exit(1)
    
    try:
        while True:
            # Read a line of data from the serial port.
            data = ser.readline()
            if data:
                #print("Received:", data)
                # Send the data over UDP.
                udp_socket.sendto(data, (UDP_IP, UDP_PORT))
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        # Cleanup resources.
        ser.close()
        udp_socket.close()

if __name__ == "__main__":
    main()