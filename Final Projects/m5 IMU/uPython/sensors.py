# sensors.py
import analogio, digitalio, board

class Pot:
    """
    Represents one potentiometer.
    
    Stores:
    - ADC reference
    - previous value (for change detection)
    """
    
    def __init__(self, pin):
        target_pin = getattr(board, f"IO{pin}")
        self.pot = analogio.AnalogIn( target_pin )
        self.prev_value = 0

    def read(self):
        value = self.pot.value >> 9
        new_value = False
        if value != self.prev_value:
            new_value = True
        self.prev_value = value
        if new_value is True:
            return value
        else:
            return False

class Button:
    """
    Represents one digital button.

    Handles:
    - Digital input setup
    - Edge detection (press / release)
    - Previous state tracking
    """

    def __init__(self, pin):
        target_pin = getattr(board, f"IO{pin}")
        print( target_pin)
        self.button = digitalio.DigitalInOut(target_pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

        self.prev_state = self.button.value

    def read(self):
        """
        Returns:
        - "pressed"
        - "released"
        - None
        """
        current = self.button.value

        if current != self.prev_state:
            self.prev_state = current
            return "pressed" if not current else "released"

        return False
    
    