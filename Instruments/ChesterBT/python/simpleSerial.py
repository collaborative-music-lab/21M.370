import serial
import socket
import sys
from serial.tools import list_ports
import time

# ------------------ Configuration ------------------
BAUD_RATE = 460800                # Serial communication baud rate.
UDP_IP = "127.0.0.1"            # Destination IP address for UDP packets.
UDP_PORT = 5010                 # Destination UDP port.
SELECTED_PORT_INDEX = 4         # Change this index to select a different port.

# ------------------ UDP Socket ------------------
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ------------------ SLIP Decoder Class ------------------
class SlipDecoder:
    def __init__(self, comm):
        """
        Initializes the SLIP decoder.
        
        :param comm: A pyserial Serial instance.
        """
        self.comm = comm
        self.inputBuffer = []   # Temporary buffer for incoming bytes.
        self.packetList = []    # List to hold decoded packets.

    def available(self):
        """
        Reads available bytes from the serial port, decodes them according to SLIP encoding,
        and, when an end byte is detected, sends the complete packet over UDP.
        
        :return: The number of complete packets awaiting further processing.
        """
        escFlag = 0
        endByte = 255
        escByte = 254
        #print('waiting', self.comm.in_waiting)
        # Process all available bytes on the serial port.
        while self.comm.in_waiting > 0:
            # Read one byte.
            val = int.from_bytes(self.comm.read(), "big")
            #print( val )
            if escFlag == 1:
                self.inputBuffer.append(val)
                escFlag = 0
            elif val == escByte:
                escFlag = 1
            elif val == endByte:
                # End of the packet detected.
                name = 'serial'
                self.packetList.append(self.inputBuffer)
                #packet type to data
                complete_packet = bytes(self.inputBuffer)
                complete_packet = name.encode('utf-8') + b':' + complete_packet
                udp_socket.sendto(complete_packet, (UDP_IP, UDP_PORT))
                #print(f"Sent UDP packet: {complete_packet}")
                # Clear the input buffer for the next packet.
                self.inputBuffer = []
            else:
                self.inputBuffer.append(val)

        return len(self.packetList)

    def get(self):
        """
        Returns the first complete SLIP-decoded packet.
        
        :return: A list of integer values representing a packet.
        """
        return self.packetList.pop(0)

# ------------------ Serial Port Selection ------------------
def get_serial_port(args):
    if len(args) > 0:
        user_port = int(args[0])
    else:
        user_port = -1  #no argument
    ports = list_ports.comports()
    available_ports = [port.device for port in ports]

    if not available_ports:
        print("No serial ports found.")
        sys.exit(1)

    print("Available serial ports:")
    for idx, port in enumerate(available_ports):
        print(f"{idx}: {port}")

    print(user_port)
    if user_port >= 0:
        if user_port < 0 or user_port >= len(available_ports):
            print(f"Serial port argument {user_port} out of range.")
            sys.exit(1)
        selected_port = available_ports[user_port]
        print(f"Selected serial port: {selected_port} (index {user_port})")
        return selected_port
    elif SELECTED_PORT_INDEX < 0 or SELECTED_PORT_INDEX >= len(available_ports):
        print(f"Invalid port index {SELECTED_PORT_INDEX}.")
        sys.exit(1)

    selected_port = available_ports[SELECTED_PORT_INDEX]
    print(f"Selected serial port: {selected_port} (index {SELECTED_PORT_INDEX})")
    return selected_port

# ------------------ Main Loop ------------------
def main():
    user_port = sys.argv[1:]
    serial_port = get_serial_port(user_port)

    # Initialize the serial connection.
    try:
        ser = serial.Serial(serial_port, BAUD_RATE, timeout=1)
        print(f"Opened serial port {serial_port} at {BAUD_RATE} baud.")
    
        time.sleep(0.1)
        print("Port open:", ser.is_open)
        print("Bytes available:", ser.in_waiting)
        print("DSR:", ser.dsr)
        print("CTS:", ser.cts)
        print("DTR:", ser.dtr)
        print("RI:", ser.ri)

        ser.write(b"hello\n")
        ser.flush()
        print("Wrote hello")

    except serial.SerialException as e:
        print(f"Error opening serial port {serial_port}: {e}")
        sys.exit(1)

    # Create an instance of the SLIP decoder.
    decoder = SlipDecoder(ser)

    try:
        while True:
            # Call available() to process any incoming data.
            packet_count = decoder.available()
            #print(packet_count)
            time.sleep(.01)
            if packet_count > 0:
                # Optionally, process the complete packet further:
                packet = decoder.get()
                # print("Received complete packet (stored):", packet)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()
        udp_socket.close()

if __name__ == "__main__":
    main()