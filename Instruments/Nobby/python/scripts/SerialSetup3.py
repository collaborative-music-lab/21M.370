import serial, serial.tools.list_ports, sys, glob
import time

class serialClass:

    # ser = 0
    inputBuffer = []
    packetList = [] 

    def __init__(self):
        pass

    def begin(self,baudrate = 460800, defaultport = "none"):
        #global ser

        #find serial port
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        #print ports
        print("available serial ports:")
        for x in range(len(ports)): 
            print(ports[x] )
        print("___")

        serial_connected = 0

        #check if cur port is available 
        if defaultport != None: 
            serial_connected = self.checkPorts(defaultport, baudrate, serial_connected)
            
        for port in ports:   
            serial_connected = self.checkPorts( port, baudrate, serial_connected )
            #
            # if defaultport in ports: port = defaultport

            # print("Looking for ESP32 on " + port)
            # try: self.comm = serial.Serial(port, baudrate, timeout=0)
            # except (OSError, serial.SerialException):
            #     print(serial.SerialException)
            #     pass
            # #setserial curSerialPort low_latency #https://stackoverflow.com/questions/13126138/low-latency-serial-communication-on-linux
            # self.comm.setDTR(False) # Drop DTR
            # time.sleep(0.022)    # Read somewhere that 22ms is what the UI does.
            # self.comm.setDTR(True)  # UP the DTR back
            # time.sleep(0.5)
            # self.comm.read(self.comm.in_waiting)
            # for i in range(10):
            #     self.comm.write([1,0,1,255])
            #     response = self.comm.read(self.comm.in_waiting) # if anything in input buffer, discard it
            #     #print(response)
            #     if len(response) > 0: serial_connected=1
            #     if serial_connected==1: 
            #         print(port + " connected\n")
            #         break;
            #     self.comm.close
            #     time.sleep(0.01)
            # if serial_connected ==1: 
            #     break;
            # else: 
            #     print(port + " not available\n") 

    def checkPorts(self, port, baudrate, connected): 
        """Check a serial port to see if there is an ESP32 connected."""
        serial_connected = connected
        if connected == 1:
            return serial_connected

        print("Looking for ESP32 on " + port)
        try: 
            #self.comm = serial.Serial(port, baudrate, timeout=0.1)  # Use small blocking timeout

            self.comm = serial.Serial(port, baudrate, timeout=0.1, rtscts=False, dsrdtr=False)
            time.sleep(0.05)  # let it settle
            self.comm.setRTS(True)
            self.comm.setDTR(False)
            time.sleep(0.1)  # keep reset low
            self.comm.setRTS(False)
            self.comm.setDTR(True)
            time.sleep(0.5)  # Wait for ESP32 to boot up and be ready

            self.comm.reset_input_buffer()  # Clear out garbage

            print(port, baudrate, serial_connected)

            for i in range(10):
                print(f"Attempt {i+1}: Sending handshake packet")
                self.comm.write([253, 1, 1, 255])  # Example command; adjust if needed
                time.sleep(0.05)  # Wait for response (adjust based on ESP32 code)

                bytes_waiting = self.comm.in_waiting
                print(f"Bytes waiting: {bytes_waiting}")

                if bytes_waiting > 0:
                    response = self.comm.read(bytes_waiting)
                    print(f"Received: {response}")
                    if len(response) > 0: 
                        serial_connected = 1 
                        print(port + " connected\n")
                        break  # Exit loop when connected

                time.sleep(0.1)  # Small pause before retrying

            if serial_connected != 1: self.comm.close()  # Correctly close the port when done

        except serial.SerialException as e:
            print(f"Serial exception on {port}: {e}")

        if serial_connected == 1:
            return serial_connected

        print(port + " not available\n")
        return serial_connected

    def available(self):
        escFlag = 0
        #constants for SLIP encoding
        endByte = 255
        escByte = 254

        while self.comm.in_waiting > 0:
            val = int.from_bytes(self.comm.read(), "big" )

            if escFlag == 1:
                self.inputBuffer.append(val)
                escFlag = 0
            elif val == escByte:
                escFlag = 1
            elif val == endByte:
                #print("endbyt", packetBuffer, self.inputbuffer)
                self.packetList.append(self.inputBuffer)
                self.inputBuffer = []
            else:
                self.inputBuffer.append(val)

        #print("inputbuffer", self.packetList)
        _available =  len(self.packetList)
        #print(_available)
        return _available

    

    def get(self):
        """Store available incoming data in inputBuffer.

        return a single slip decoded message."""
        return self.packetList.pop(0)#remove and return first element of list

    def slipDecodeData(self, data ):
        #print("slipinput",data)
        """Slip encode data and add to output buffer."""
        inputBuffer = []
        escFlag = 0
        for i in data:
            if escFlag == 1:
                inputBuffer.append(i)
                escFlag = 0
            elif i == self.escByte:
                escFlag = 1
            elif i == self.endByte:
                return inputBuffer
            else:
                inputBuffer.append(i)

        return inputBuffer


    def send( self, data ):
        #print("serial.send", data )
        self.comm.write(bytearray(data))


