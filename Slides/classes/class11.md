
# Sensors I

21M.370 

Digital Instrument Design

Ian Hattwick

---

## References

All references in Canvas unless a link is provided

Baalman, Marije. “Sensors”. Just a question of mapping. 2021.

---

## Sensors and musical interaction 

What kinds of gestures do we use to perform?
What kinds of physical data can we use to capture performances?
What kinds of sensors work well?
What kinds of gestures are suggested by new sensors?

---

## Musical gestures

physical position
- waving, XYZ coordinates, 
interaction with a surface
- pressure, strike
physical movement, rotation
blowing, static air pressure
force, impulse
strumming, bending
biosignals
- EMG, EEG, Heartrate, GSR, Breath/diaphgragm, 
sliders

---

## Musical gestures

swiping 
- spatial metaphor 
- semantic 
conductor gestures 
- energy 
- open air
touch and sliding
head nodding

pluckings
striking
blowing
kicking
pressing
bowing
squeezing
singing / speaking

---

## Pots vs encoders

Potentiometers: 
- have a fixed physical range 
- generally use a single range of values mapped to pot range
Encoders 
- endless rotation 
- current position calculated in software based on change in rotation 


---

## Pots vs encoders

Potentiometers: 
- how to allow for saving presets? 
- physical motion: https://youtu.be/sV9Im_zvea0 
- rotocontrol
Encoders 
- allows for changing mapping without discrepancy between pot value and mapped value 
https://youtu.be/COVNwdMld8Q 
- abstraction allows for interesting algorithms: 
https://youtu.be/HM0EBvJe1s0

---

## Buttons

Discrete  / Buttons 
- mechanical switch 
- solid-state switches (Hall, optical, etc.)
Measuring physical motion 
- Elevator buttons: 
  https://www.langir.com/19mm-piezo-switch/ 
  https://www.langir.com/category/capacitive-switch/ 
- Velocity: measuring time vs distance or pressure

---

## Keyboards

MIDI Polyphonic Expression (MPE) 
- how to detect 3D gestures?
Haaken Continuum: hall effect sensors 
https://www.youtube.com/watch?v=SiAb48qsZHY&t=1077s 
https://youtu.be/PnBhR8RLJN
LinnStrument: Force Sensing Resistor 
https://youtu.be/MDTikW1BFt8

---

## Hall Effect sensors

Measure small motion with great precision 
- very repeatable 
- insensitive to external conditions (except heat?) 
https://www.emobility-engineering.com/hall-effect-sensors/ 
- direct voltage output
Mechanical design considering magnetic field orientation and magnet placement and travel. 
 
 
---

## Force Sensitive Resistors (FSR)

Use in voltage divider
Mechanically simple 
- subject to hysteresis
Expensive in small quantities
Fragile 
- soldering to pins 
- bending 

Also similar: bend and flex sensors

Example: keith mcmillen instruments
https://www.keithmcmillen.com

---

## Piezo discs

Create an instantaneous voltage when deformed.

Often used as impact sensors for drum kits

Create an acoustic wave which has to be analyzed and converted into a trigger signal with a micro controller.


<div class="image-wrapper">
<img src="https://www.he-shuai.com/wp-content/uploads/2021/02/piezoelectric-ceramic-buzzer-disc550.jpg" class="large-img"/>
</div>


---

## Optical Sensors

Cheap-and-cheerful: photocells 
- Cadmium sulfide (Cds) 
https://youtu.be/KlUua1Livuw

Displacement in controlled environment 
https://youtu.be/EZdgr6sLQ1Q

Measurement of motion 
- optical encoder

Infrared sensors
- emitters and detectors

---

## Other sensors

Distance sensors
* Laser ToF sensors
* ultrasound

computer vision based sensors
- Color sensor
- low resolution cameras
- high resolution cameras

Motion Sensors
* Accelerometers
* 9 DoF boards

Biosensors

