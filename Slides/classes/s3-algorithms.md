# 21M.370 Algorithms

What is an 'algorithm'?

<br>

Why are they useful?

---

# Musical abstractions

* What abstractions do we commonly use?



---

# Algorithm types

* Deterministic vs stochastic. Does the algorithm depend on random elements, or will it always give the same output for the same set of inputs?
* Rule or grammar based, vs self-contained
* Generative or 


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
- 7th chord (1,3,5,7) = `scale[0],[2],[4],[6]`
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

## Simple algorithm: chord machine

* User input: root
* Global data: key
* Output: Chord built on root in that key

Stretch goal:
* Arpeggiator
	* on each beat output one note from the chord
	* how to select which note per beat?
	* creative options?

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

## euclidean algorithm

For:
* `n = number of hits`
* `l = number of beats`
* create `n` buckets of size `l` 
* for `l` elements:
	* add `n` to the first free bucket
	* if this overflows the bucket size:
		* put the overflow in the next bucket
		* return 1
	* else return 0

---


<img src="./images/euclid/euclid0.jpg">


