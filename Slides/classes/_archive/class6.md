
# m370 breakout and sensors

21M.370 

Digital Instrument Design

Ian Hattwick

---

## Class on zoom on monday

I'll send zoom link

we will review this week's reading then

---

## Lab 3

Now available

---

## References

All references in Canvas unless a link is provided
* Baalman, Marije. “From one range to another”. Just a question of mapping. 2021.
* Todd, Carl. Online Potentiometer Handbook. 1975

---

## 21M.370 Breakout

<img src="./images/breakout.jpg" class="full-img"/>

---

## 21M.370 Breakout

<img src="./images/breakout-graphic.png" class="full-img"/>

---

## 21M.370 Breakout

* Analog pins: 0-5
* Digital Pins: 6-9 plus 11 and 13
* I2C pins
* SPI pins not connected
* 5v I2C pins for special cases

<div class="image-wrapper">
<img src="./images/breakout-graphic.png" class="medium-img"/>
</div>

---

## Analog Signals

Electrical signals measured in Volts.
* range is from 0v to VCC, either 3.3v or 5v depending on microcontroller
* ESP32 uses 3.3v

Buttons: 
* either high or low (0,1) (True,False)

<div class="image-wrapper">
<img src="./images/voltage-divider.png" class="medium-img"/>
</div>

---

## Potentiometers

Variable resistor with three taps:
*  two taps connected to either end of a resistor
*  the third is a ‘wiper’ which travels along the resistor
Used as a voltage divider:
*  the voltage at the wiper is proportional to the distance between the wiper and the ends of the resistor

<div class="image-wrapper">
<img src="./images/pot-schematic.png" class="medium-img"/>
</div>
---

## Potentiometers

<img src="./images/pot-diagram.png" class="full-img"/>

---

## Analog to Digital

ADC  
* bit resolution, how many bits will it use to represent voltage:
* e.g. 
	* 8-bit 0-255 
	* 10-bit 0-1023
	* 12-bit 0 -4095

---

## Digital signals

UART: Serial signal like USB
*  fixed rate
*  bidirectional with TX and RX lines
I2C:
*  communication bus allowing lots of devices on same bus
*  CLK and SDA lines
SPI:
*  higher speed 
*  MOSI, MISO, CLK, SELECT lines 

---

## Digital Protocols

MIDI - musical instrument digital interface
*  simple protocol using 3 byte packets:   [status] [address] [data]
*  each byte has 1-bit type indicator and 7 data bits
OSC
*  human-readable using ASCII addresses and data
*  any data type / range

---

## Digital Protocols

MIDI
*  low resolution 0-127
*  non-human readable
*  designed for hardware communication
*  compact/efficient
OSC
*  inefficient due to ASCII
*  optimized for high speed networks

---

## Ranges

* Analog Voltage: 0-3.3v
	* ESP32 ADC resolution 0-4095
	* Python analog read is 16-bit for some reason
* MIDI: 0-127
* OSC: any
* Frequency: 20-20,000 Hz Amplitude: 0-1 Time: seconds

Easy way of reducing bits: the `>>` bitwise operator
* moves the value N bits to the right
* removes lowest bits
* `11010111 >> 4` becomes `1101`

---

## Scaling

Generic scaling: 

<div class="image-wrapper">
<img src="./images/scaling.png" class="full-img"/>
</div>

Doesn’t clip output
* think of how curve would affect a range of 0-1
* outside of that range things can get screwy!

---

## Clipping

What happens when a value goes out of range?
*  gets limited to range
*  or is allowed to exceed range
Too much clipping can lead to flat response
*  sometimes unexpected behaviour at extremes can be interesting!
Design systems to tolerate wide values, even if they become unpredictable
