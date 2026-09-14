# Frequency, Pitch, and Signals

In Automatonism & PureData
---

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
- makes all notes 'slightly' out of tune
- but all chords have the same ratios!
- often called **12-TET**
  - 12-tone equal temperament

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
## Musical scales

Mostly we don't use the chromatic scale as-is
- we create other scales as subsets 
- Major scale: [0,2,4,5,7,9,11] (Ionian)
- Minor scale: [0,2,3,5,7,8,10] (Aeolian)
- Pentatonic scale: [0,2,4,7,9]

Chords are typically every other note of a scale,
- Major chord: [0,4,7]
- Minor chord: [0,3,7]

Referencing scales by *scale degree*
- Triads (1,3,5) = scale[0],[2],[4]
- 7th chord (1,3,5,7) = scale[0],[2],[4],[6]
---

## Triad representations

Represented as scale degrees:<br>

| Major Triad  | 0 |   |  |  | 2 |  |  | 4 |  |  |  |  | 7 |
|--------------|---|---|---|---|---|---|---|---|---|---|----|----|----|
| Major scale  | 0 |   | 1 |   | 2 | 3 |   | 4 |   | 5 |    | 6  | 7  |

Represented as chromatic degrees:<br>
| Major Triad  | 0 |   |  |  | 4 |  |  | 7 |  |  |  |  | 12 |
|--------------|---|---|---|---|---|---|---|---|---|---|----|----|----|
| Major scale  | 0 |   | 2 |   | 4 | 5 |   | 7 |   | 9 |    | 11  | 12 |
| Chromatic   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |

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
