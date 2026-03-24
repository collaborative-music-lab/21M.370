
# Sensor Processing

21M.370 

Digital Instrument Design

Ian Hattwick

note:
Testing

---

## Upcoming schedule

* Monday: 
	* Readings 
	* Micro Lecture
	* Performance?
* Wednesday (voxel) 
	* Andi Otto
	* Grad presentations
	* Lab 5 performances
	* Lab 5 assemble MPR121
* Spring Break!
* Monday Mar 28 (online): 
* Wednesday Mar 30 (voxel):

---

## References

All references in Canvas unless a link is provided

https://hackaday.com/2015/12/09/embed-with-elliot-debounce-your-noisy-buttons-part-i/
<br>
Baalman, Marije. “From one range to another”. Just a question of mapping. 2021.

---

## Sensor Signal Processing

How do we turn raw sensor data into signals that represent our actions?

How do we prevent false triggers or erroneous data?

What kinds of gestural data are useful?

<div class="image-wrapper">
<img src="https://interactivetextbooks.tudelft.nl/qsm/_images/sensor_noise.PNG" class="large-img"/>
</div>




---

## Potentiometers and Buttons

* packages containing a sensor and a hardware interface
* designed with a clear gesture in mind
* physical form factor lends itself to easily mounting to an enclosure
* physical characteristics consider human factors

<div class="image-wrapper">
<img src="https://components101.com/sites/default/files/components/Different-Types-of-Potentiometers.jpg" class="large-img"/>
</div>

---

## Discrete Signals

Either 0/1, up/down
<br>

Useful states: 
- Down - transition from up to down 
- Pressed - constant value of 1 
- Up - transition from down to up 
- Released - constant value of 0
Need to remember previous state to compare 


---

## Discrete Signals

Possible errors: 
- mechanical bounce: button contact ‘chatter’s when pressed, creating a series of on/off values
Debounce techniques: 
- forced delay: prevent  
  retriggers until N ms 
- lowpass filter & schmitt trigger 
- pattern filtering

<div class="image-wrapper">
<img src="https://hackaday.com/wp-content/uploads/2015/11/debounce_bouncing.png?resize=800,280" class="large-img"/>
</div>

---

## Schmitt Trigger


Schmitt trigger 
- separate thresholds for up  
  and down states 
- very standard for discrete  
  inputs

<div class="image-wrapper">
<img src="./images/schmitt_trigger.png" class="large-img"/>
</div>


---

## Pattern Matching

Pattern matching 
- look for patterns over time to determine state 
- create array of values [oldest, . . . . , newest] 
- ideal patterns: 
- [00000001]    is change from low to high 
- [11111110]    is change from high to low
Real world patterns 
- [00000001] instantaneous change when button is pressed 
- [10010100] possible pattern when releasing with bounces 
- [10000000] identify release only at end of button bouncing 

<div class="image-wrapper">
<img src="./images/noisy_button.png" class="med-img"/>
</div>
 

---

## Discrete Signals

Issues: 
- when is button state change identified?  
- lowpass filters add latency 
- pattern matching may add latency 
  - latency on releases less important than presses?
Other modalities 
- double-click 
- long/short press 
- length of button press as signal


---

## Continuous signals

Interest in range of values related to a gesture

Potentiometer: 
- gesture of turning a knob related to output signal 
- problems: incomplete range, noisy signal

Capacitive sensor 
- range of values may constantly change 
- no clear limit to range of values 
- very noisy

---

## Continuous signals

One-pole lowpass filter 
`y[n] = a * x[n] + (1 - a ) * y[n-1], a=smoothing value `
- high values of *a* give less smoothing
- It uses a feedback loop, so the calculation needs to run continuously - e.g., it needs to get called every loop
- easy and effective for simple noise

<div class="image-wrapper">
<img src="./images/onepole_code.png" class="large-img"/>
</div>

---

## Continuous signals

processing a window of values 
- store an array of N values 
- push new data to array and remove oldest element
- then process entire array

Moving average: take average of array 
- similar to lowpass filter but more complicated/ takes more memory
- good for generally noisy signals

---

## Median Filter

Median filter 
- removes high and low values 
- good at removing noise spikes

<div class="image-wrapper">
<img src="https://miro.medium.com/v2/resize:fit:1400/1*pXL2mSo47CDzxsg-Fd84XA.png" class="large-img"/>
</div>

---

## Ranges

Generic scaling: 

<div class="image-wrapper">
<img src="./images/scaling.png" class="large-img"/>
</div>

Doesn’t clip output
think of how curve would affect a range of 0-1 
- outside of that range things can get screwy!


---

## Clipping

What happens when a value goes out of range? 
- gets limited to range 
- or is allowed to exceed range
Too much clipping can lead to a boring experience
- sometimes unexpected behaviour at extremes can be interesting!
Design systems to tolerate wide values, even if they become unpredictable

Curve = 1
<div class="image-wrapper">
<img src="./images/clipping.png" class="large-img"/>
</div>

Curve = 2
<div class="image-wrapper">
<img src="./images/curve_exponential.png" class="large-img"/>
</div>


