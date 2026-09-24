# 21M.370 Class 3

* Mari Kimura reading
* Signals in DMIs
* Euclidean Algorithm
* Lab 1 check-in

---

# Mari Kimura!

Wednesday Sept 23 Mari Kimura will be visiting campus to give a lecture
She will visit 21M.370

* W18-1311 at 2:30-3:30

So we will stay in W18-1311 for that day
* next wednesday in Voxel for sure!

---

# Reading

---

# Signals in DMIs

Lots of different signals
* Types: analog, digital, numeric, semantic, serial, packetized
* Sources: 
	* analog sensors - voltage (0-3.3v)
	* digital sensors - serial stream
	* analog-to-digital conversion: representation of an analog signal, quantized to bit-depth
		* 8-bit: 0-255 (2^8 = 255)
		* 12-bit: 0-4095 (2^12 = 4096)
	* MIDI data: 7-bit (0-127)
	* Musical parameters:
		* Frequency (Hz)
		* Time (seconds)
		* Amplitude (0-1)
		* Decibels (-infinity to 0)
		* Other arbitrary unit . . .

---

# Numeric vs semantic

* numeric: typical for most continuous data streams, signals
	* Easy to parse and process values (because math)
	* what happens when one byte doesn't contain the whole value?
		* e.g. two 8-bit values represent a 16-bit value
	* what happens when the signal contains multiple values?
		* e.g. [frequency, amplitude]
* semantic:
	* human readable, easy to conceptualize routing
		* `basic-osc 1 PITCH 400`
	* Takes more data (ASCII encoding), bandwidth limitations
		* USB can be sloooooow
		* different computers or software process things more or less efficiently
	* harder to process algorithmically
		* need to parse where the numeric value is, or ???

---

# Serial vs packetized

* Serial:
	* constant stream of numbers, sent one at a time.
		* Often byte streams (USB)
	* Needs to be parsed somehow:
		* what signal does this stream represent?
		* if multiple bytes represent on event, how do we group bytes together?
			* USB is 8-bit natively
	* often needs to converted to packets
* Packetized:
	* groups of values
		* often semantic and numeric
		* `[basic-osc, 1, PITCH, 100]`
	* need to have a consistent structure for parsing
		* often have conventions, but you can define your own 
	* can contain different kinds of data
		* e.g. pitch, amplitude, timbre, envelopes

---

# What are our signals?




---

# Frequency, Pitch, and Signals

**Frequency and Musical Pitches**
- Frequency is in cycles per second (cps)
  - or Hertz
- Pitches are defined as ratios
  - often relative to a 'root'
  - 'A440' is the pitch reference for orchestras

---
## Just Intonation

Pythagoras gets credit for discovering:
- simple ratios create pleasing intervals
- octave: [2/1]
- Major chord: [1, 5/4, 3/2]
- Major scale: [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2/1]
- These simple ratios are called **Just Intonation**

---
Chromatic scale:
<small>
| Interval   | Degree | Ratio  |
|------------|--------|--------|
| Root       | 0      | 1/1    |
| Minor 2nd  | 1      | 16/15  |
| Major 2nd  | 2      | 9/8    |
| Minor 3rd  | 3      | 6/5    |
| Major 3rd  | 4      | 5/4    |
| Perfect 4th| 5      | 4/3    |
| Tritone    | 6      | 45/32  |
| Perfect 5th| 7      | 3/2    |
| Minor 6th  | 8      | 8/5    |
| Major 6th  | 9      | 5/3    |
| Minor 7th  | 10     | 9/5    |
| Major 7th  | 11     | 15/8  |
| Octave     | 12     | 2/1    |

Note: there are many variations of just-intoned scales
- each trying to 'fix' bad intervals!

</small>

---
## The transposition problem

A major chord built on the root sounds good:<br>
`[0,5/4,3/2] = [1, 1.25, 1.5]`

A major chord built on the 5th sound good:<br>
`[3/2,15/8,18/8] = [1.5, 1.875, 2.25] = [1, 1.25, 1.5]` 

A major chord built on the 3rd, not so much<br>
`[5/4,8/5,15/8] = [1.25, 1.6, 1.875] = [1, 1.28, 1.5]`

---

| Root | Root    | Third   | Fifth   |
|------|---------|---------|---------|
| C    | 1.00    | 1.25    | 1.50    |
| C#   | 1.00    | 1.25    | 1.50    |
| D    | 1.00    | 1.25    | 1.48    |
| D#   | 1.00    | 1.25    | 1.50    |
| E    | 1.00    | 1.28    | 1.50    |
| F    | 1.00    | 1.25    | 1.50    |
| F#   | 1.00    | 1.28    | 1.517   |
| G    | 1.00    | 1.25    | 1.50    |
| G#   | 1.00    | 1.25    | 1.50    |
| A    | 1.00    | 1.28    | 1.48    |
| A#   | 1.00    | 1.28    | 1.50    |
| B    | 1.00    | 1.25    | 1.50    |


---
## Equal Temperament

'Tempers' the fifth by flatting it slightly
- makes all notes 'slightly' out of tune, but all chords have the same ratios!
- often called **12-TET**,  12-tone equal temperament

The formula: ratio = 2^(N/12)
- where N is the # of half-steps
- 2^(1/12) = 1.059
- 2^(4/12) = 1.2599
- 2^(7/12) = 1.498
- 2^(12/12) = 2.0

what frequency in Hz is middle C?
A = 440
C = 9 steps below A
2^(-9/12) * 440 = ??

---
## MIDI notes

Musical instrument digital interface
- established in 1983
- standard protocal for sending musical data

MIDI pitches
- chromatic pitches 0-127
- MIDI note 60 is middle C
- an octave is 12, so C=[36,48,60,72]
- easy way to think and work with notes

---
## Analog pitch representations

Analog synthesizers represent pitch as *voltage*

Two standards:
- 1V / octave
  - linear pitch, exponential frequency
  - each volt goes up an octave
  - most common, by far
- Hertz / volt
  - linear frequency
  - exponential pitch, octaves = [0.5,1,2,4] 


---
## Automatonism pitch representation

Represents full MIDI note range (0-127) as (0-1)
- each chromatic note increases by 1/127
- an octave is 12/127
- quantizers output a few octaves

But how do we represent just intonation?
- we have to reverse engineer from 12-tet!
- 12-TET: ratio = 2^(N/12)
- Automatonism octave: 12/127 = 0.09449... 
- Just formula: `log2(ratio) * (12/127)`
- let's do this in python...

---

<img src="./images/pd-tuning.png" class="large-img"/>

---

## Automatonism oscillators

* Pitch input expects (0-1) values
* Pitch *slider* is in MIDI notes!
* FM (frequency modulation) input is ???
* Filter cutoff inputs are ???
* Don't worry about it!

<img src="./images/pd-wtable.png" class="medium-img"/>

---

## Signals and control messages

Audio needs to be continuously generated
- 48000 values per second!
- requires dedicated signals
- all automatonism modules are audio!!!
- in PD: thick lines, modules use `~` tilde

<img src="./images/pd-signals.png" class="small-img"/>

Control messages are only sent when triggered
- 1 message per trigger
- in PD thin lines
- convert to audio using `sig~`
- all messages outside PD are control rate!

---

## Control Automatonism parameters

**MOST** parameters for automatonism modules can be easily controlled remotely

You target a parameter by:
* module name (lowercase)
* module instance number
* parameter name (CAPITALS)


Modules with the same name and instance number receive the same messages!

<img src="./images/pd-remote-msg.png" class="large-img"/>

