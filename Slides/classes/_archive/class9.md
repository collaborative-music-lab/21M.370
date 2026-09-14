
# Musical Algorithms

21M.370 

Digital Instrument Design

Ian Hattwick

---

## Types of control

The kind of control that we have determines how we think about performing.

<br>

Continuum: Direct control of events versus high-level structuring

---

## Note Events

* traditional approach to music performance
* discrete gesture is for triggering notes
* continuous gestures to shape tmbre over time

Classic keyboard model

---

## Sequencing

Standard model for working with synthesizers
* fixed length cycle
* each step has controls for pitch and enable
* interaction takes form of selecting pitch and switching enables on and off (e.g. rhythm)

<br>

By default sequencers are the same length and synchronized
* beginning of sequence start at the same time
* unsynchronized sequences allow for more complex patterns
* variable lengths allow for more complex patterns

---

## algorithmic controls

Generating musical events determined by the output of algorithms is a common approach
* allows for complex output with only a few input parameters
* can either be used to generate a fixed length sequence, or can be used to continuously generate new notes
* the challenge is to create musically interesting and appropriate patterns

---

## euclidean sequencing

the process of distributing $n$ pulses across a grid of $l$ steps such that the pulses are as equidistant as possible

https://ianhattwick.com/examples/euclid.html

The beauty is that the resulting rhythms are musically useful, and common across styles of music around the world.

Parameters:
- steps: the number of beats of the sequence
- hits: the number of events distributed in the sequence
- rotation: an offset for the beginning of the sequence 

---

## mathematical generation of events

It is possible to generate events by using simple, mathematical formulas.
* typically the formulas take an input variable *t* which represents the current beat number
* trigonometric formulas often work well to create repeating patterns with internal structure
* but obviously there are a lot of other approaches


