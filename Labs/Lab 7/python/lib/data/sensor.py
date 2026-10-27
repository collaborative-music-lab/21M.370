# sensor.py
import math, time

def _coef(tau, dt):
    """Time constant in seconds -> one-pole smoothing coefficient."""
    if tau <= 0:
        return 1.0
    return 1.0 - math.exp(-dt / tau)


class Sensor:
    """
    Generic sensor class. Call update(raw) once per loop.

    Parameters:
    - alpha: smoothing coefficient. Can be a single value or an array [rising, falling]
    - gate:  sets the output to 0 if its abs() is lower than the gate value.
      assumes that the base value of the signal is around 0
    - invert: inverts the incoming signal
    """

    def __init__(self, alpha=0.5, gate=0, invert=False):
        self.enable = True
        self.value = None
        self.alpha = alpha
        self.gate = gate
        self.invert = invert
        self.output = None
        
    @property
    def alpha(self):
        return (self.alpha_rising, self.alpha_falling)

    @alpha.setter
    def alpha(self, alpha):
        if isinstance(alpha, (list, tuple)):
            self.alpha_rising, self.alpha_falling = alpha
        else:
            self.alpha_rising = self.alpha_falling = alpha
        
    def update(self, x):
        if not self.enable: return None
        
        if self.invert:
            x = -x

        if self.value is None:
            self.value = x
        else:
            a = self.alpha_rising if x > self.value else self.alpha_falling
            self.value = a * x +  (1-a) * self.value
        
        return self.get()
    
    def get(self):
        if not self.enable: return None
        
        if self.gate > 0:
            if self.value > 0: self.output = self.value - self.gate
            else: self.output = self.value + self.gate
            return 0 if abs(self.value) < self.gate else self.output

        return self.value
        
        



