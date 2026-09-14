
# Musical Algorithms

21M.370 
<br>
Digital Instrument Design
<br>
Ian Hattwick

---

## Problems and Prospects for Intimate Musical Control of Computers

David Wessel, Matthew Wright; Problems and Prospects for Intimate Musical Control of Computers. Computer Music Journal 2002; 26 (3): 11–22. 

* immense timbral freedom of computers
* ‘one-gesture-to-one-acoustic-event’
* Low ‘‘Entry Fee’’ with No Ceiling on Virtuosity
* 10ms latency requirement
* Control Gestures as Events and Signals
* Musical Features all instrument should have
* Metaphors for musical control
* Open Sound Control



---


<img src="./images/wessel_dmis.png" class="full-img"/>

> David Wessel, Matthew Wright; Problems and Prospects for Intimate Musical Control of Computers. Computer Music Journal 2002; 26 (3): 11–22.

---

## different types of mappings

* one-to-one mapping: one gesture controls one sonic event
	* trigger a note
	* use a knob to control filter cutoff
* one-to-many 
	* violin bow - controls volume, timbre, other
	* MPE controller: X:pitch, Z:volume, Y:timbre
* many-to-one
	* violin volume
	* filter cutoff: knob position, keytracking, lfo, envelope

---

## Types of gestures

Discrete Events
* keyboard press
* Any note on event
* percussive strike

Semi-discrete
* continuous change, then static value
* Knob positions

Continuous gestures
* gestural value only valid during the gesture itself
* change is the point of interest
* violin bow
* hand gesture in space
* gestural control of a potentiometer

---

## Proposed gestural metaphors

* spatial metaphors
* drag and drop
* scrubbing
* dipping
* catch and throw


---

## spatial metaphors

<div class="image-wrapper">
<img src="./images/macadams_timbreSpace.png" class="large-img"/>
</div>

> S. McAdams. K. Siedenburg et al. (eds.), Timbre: Acoustics, Perception, and Cognition,
Springer Handbook of Auditory Research 69, 2019.

---

## dipping

* the computer constantly generates musical material via a musical process, but this material is silent by default
* performer controls the volume of each process
* each musical event can be precisely timed, regardless of the latency or jitter of the gestural interface
* its rhythm is not dependent on the performer in an event-by-event way

---

## more general algorithms

* euclidean sequencing
* geometric functions to generate events or control streams
* terrain traversal
* markov models
* shaped / constrained randomness
* what other ideas?

---

## Metaphors

DJs
* start with source material
* transforming material
* think compositionally over time 
* disconnect between gesture and steady sound
* do things hidden
* preparation
* scratching 
* timbral control
* catch and throw
* responsible for the whole mix

Piano
* start with a piano score
* gestural commitment
* gestual detail
* not a lot hidden
* fairly consistent timbre

Electric Gtr
* gtr, amp, effects pedals
* delay and time based effects as part of the sound

Production
* loop based performance
* mixing as performance
* production as key element
* short clips arranged in time
* visual metaphors
* humanizing as a conscious act

---

# Options for Nobby

* Find a way to implement rotation
* Decay time and amplitude for voices
* change the way that synth sequeces are generated










