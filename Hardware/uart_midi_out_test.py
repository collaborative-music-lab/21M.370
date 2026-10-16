# Example code to test a hardware UART MIDI output

import board
import busio
import time

class UART_MIDI:
    """
    A simple UART MIDI output class for CircuitPython on ESP32-S3.
    Sends MIDI messages over UART.
    """
    
    # MIDI Status Bytes (for Channel 1, 0x00-0x0F for channels 1-16)
    NOTE_OFF = 0x80
    NOTE_ON = 0x90
    CONTROL_CHANGE = 0xB0
    
    def __init__(self, tx_pin=board.IO1, baudrate=31250):
        """
        Initialize UART MIDI output.
        
        Args:
            tx_pin: GPIO pin for UART TX (default: pin 1/IO1 on ESP32-S3)
            baudrate: MIDI baudrate (standard is 31250)
        """
        # UART1 on ESP32-S3 with TX on pin 1
        # Note: You need an RX pin too, even if not used. Pin 2 is commonly paired with pin 1
        self.uart = busio.UART(
            tx=tx_pin, 
            rx=board.IO2,  # RX pin (can be unused but must be defined)
            baudrate=baudrate,
            timeout=0.001
        )
        self.channel = 0  # MIDI Channel 0 (Channel 1 in MIDI terminology)
    
    def note_on(self, note, velocity=100, channel=None):
        """Send a Note On message."""
        if channel is None:
            channel = self.channel
        
        status = self.NOTE_ON | (channel & 0x0F)
        note = max(0, min(127, note))
        velocity = max(0, min(127, velocity))
        
        # Reverse bits for correct MIDI transmission
#         self.uart.write(bytes([
#             self._reverse_bits(status),
#             self._reverse_bits(note),
#             self._reverse_bits(velocity)
#         ]))
        message = bytes([status,note,velocity ])
        print(message)
        print("Sending bytes (binary):")
        for i, byte in enumerate(message):
            print(f"  Byte {i}: {bin(byte)} (0x{byte:02X})")
        self.uart.write(message)
#         self.uart.flush()  # Wait for transmission to complete
        print(f"Note On: note={note}, velocity={velocity}, channel={channel}")
    
    def note_off(self, note, velocity=0, channel=None):
        """
        Send a Note Off message.
        
        Args:
            note: Note number (0-127)
            velocity: Release velocity (0-127)
            channel: MIDI channel (0-15, overrides default if specified)
        """
        if channel is None:
            channel = self.channel
        
        status = self.NOTE_ON | (channel & 0x0F)
        note = max(0, min(127, note))
        velocity = max(0, min(127, 0))
        
        self.uart.write(bytes([status, note, velocity]))
        print(f"Note Off: note={note}, velocity={velocity}, channel={channel}")
    
    def control_change(self, cc_number, value, channel=None):
        """
        Send a Control Change (CC) message.
        
        Args:
            cc_number: CC number (0-119)
            value: CC value (0-127)
            channel: MIDI channel (0-15, overrides default if specified)
        """
        if channel is None:
            channel = self.channel
        
        status = self.CONTROL_CHANGE | (channel & 0x0F)
        cc_number = max(0, min(119, cc_number))
        value = max(0, min(127, value))
        
        self.uart.write(bytes([status, cc_number, value]))
        print(f"CC: cc={cc_number}, value={value}, channel={channel}")
    
    def set_channel(self, channel):
        """Set the default MIDI channel (0-15)."""
        self.channel = max(0, min(15, channel))
        
    def _reverse_bits(self, byte):
        """Reverse the bit order of a byte (LSB ↔ MSB)."""
        result = 0
        for i in range(8):
            result = (result << 1) | (byte & 1)
            byte >>= 1
        return result
    
    def close(self):
        """Close the UART connection."""
        self.uart.deinit()

midi = UART_MIDI(tx_pin=board.IO5, baudrate=31250)
midi.set_channel(1)

# print(f"Baudrate: {midi.uart.baudrate}")
# print(f"Bits: {midi.uart.bits}")
# print(f"Parity: {midi.uart.parity}")
# print(f"Stop bits: {midi.uart.stop}")

index = 0

while True:
     # Play a simple melody
    notes = [60, 72, 48]  # C, D, E, F, G
    
#     index = (index+1) % len(notes)
#     note = notes[index]
    
    index = (index+10) % 127

    midi.note_on(48, velocity=index)
#     midi.control_change(cc_number=1, value=index*10)    # Modulation
    time.sleep(0.5)
#     midi.note_off(note)
#     time.sleep(0.5)

