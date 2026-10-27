
# Timing

21M.370 

Digital Instrument Design

Ian Hattwick

---

# Reference

All references in Canvas unless a link is provided

Chris Wilson. “A Tale of Two Clocks”.

https://web.dev/articles/audio-scheduling

[Anne Danielson. "Here, There, and Everywhere: three accounts of pulse in D’Angelo’s ‘Left and Right’"](https://www.researchgate.net/publication/262102942_Here_There_and_Everywhere_three_accounts_of_pulse_in_D'Angelo's_'Left_and_Right')


---

# Schedule

Nobby perfomances:
Oct 26
Oct 28

Capacit performances
Oct 28
Nov 2
Nov 4

Andi Otto Nov 9 & 23

Performer presentations
- was Nov 9 & 16
- either Nov 2 & 4 or Nov 16 & 18

---

# Kinds of time

Musical time 

<div class="image-wrapper">
<img src="./images/musical-timing.png" class="large-img"/>
</div>


---

# Kinds of time

Musical time 

- how music is actually played
- generally beat-based 
- includes larger groupings (bars, phrases) 
- can be tight or loose 
- relationships between events is important! 
- groove and feel depend on timing, tone, phrasing, etc.

---

# Kinds of time

Real time: all instruments have time responses, often experienced as the ‘feel’ of an instrument 

Mechanical speed: piano: travel of key and hammer action
Sound travelling through the air: Physical speed of sound ~343m/s 
- french horn: 4m of tubing = 4/343 = 0.011s 

<div class="image-wrapper">
<img src="./images/instrument-waveforms.png" class="large-img"/>
</div>


---

# Kinds of time

Computer time 
- discrete time 
- processes audio in samples, e.g. 48kHz 
- requires precision (no jitter) and NO DROPOUTS

In a computer there are two kinds of clocks: 
- general purpose clocks: unpredictable timing 
- audio clocks (sample-accurate): guaranteed timing

<div class="image-wrapper">
<img src="./images/jitter-audio.jpg" class="medium-img"/>
</div>


---

# Kinds of time

Audio Buffers 
- provide protection against dropouts 
- minimize CPU cost 
- collection of audio samples, powers of 2

Types of buffers 
- analog-digital converter (ADC) 
- internal software DSP buffer 
- digital-analog converter (DAC) 

Buffers sacrifice latency for stability

<div class="image-wrapper">
<img src="./images/audio-buffers.jpg" class="medium-img"/>
</div>



---

# Kinds of time

Digital communication standards
- UART: Universal Asynchronous Receiver/Transmitter
	- An asynchronous serial link with no shared clock
	- both ends agree on a baud rate and frame each byte with start and stop bits.
	- common speeds: 9600 - 921600 bits/second (BAUD)
- I2C: Inter-Integrated Circuit (written I²C, pronounced "I-squared-C")	
	- A two-wire (SDA data, SCL clock) synchronous bus that lets multiple devices share the lines, each addressed individually.
	- 100-400 kbits/second
- SPI: Serial Peripheral Interface	
	- A synchronous, full-duplex bus that uses a shared clock, separate MOSI and MISO data lines, and a chip-select line per device.
	- 1 to 50 MHz

---


# Kinds of time

Digital communication standards

Communication 
- often times not optimized for real-time interaction 
- UART / USB 2.0: sends data at bits/second (BAUD rate)
- microcontrollers generally use a UART-USB chip which has its own buffers / latency (but not our class-compliant ESP32s3!)

Digital communication standards

Generally, wired and local network comms are OK

Wireless often adds unacceptable latency UNLESS specifically designed for music, e.g. MIDI BLE

---

# Real-time performance

Latency is how quickly sound is generated in response to action 
- ~10ms is considered acceptable . . .  
- low jitter is also important

Components: 
- ESP32: execution speed, UART communication 
- CP2104: USB communication chip 
- Python: data processing, OSC messages 
- PD: DSP processing, Audio output

<div class="image-wrapper">
<img src="./images/pd-buffer.png" class="medium-img"/>
</div>


---

# Automating time

Keeping good time is hard! 
- lots of reasons for latency/ jitter 
- being a good musician takes practice!

Computers (can be) good at keeping time 
- to guarantee timing accuracy, event timing should be tied to audio clock 
- typically python,javascript,etc timing isn’t consistent 
- SCAMP in python has a good audio clock
- PD has two types of signals: audio and control 
- automitonism uses audio clock for triggers

---

# Automating time

Beat clocks: 
- generally pulses-per-quarter-note (ppqn) 
- analog: 1 ppqn 
- MIDI: 24 ppqn 
- how to schedule ‘off-the-grid’?

phrase synchronization 
- how to make multiple sequencers play together? 
- reset on downbeats (every 8,16,32, etc. beats)

---

# Automating time

Integer clock counters 
- increment by 1 every pulse 
- sequencers use modulo to determine index,  
   e.g. clock%8 for an eight-step sequence

Schedulers 
- sequencers schedule an event in the scheduler 
- allows for adjustments to scheduled times

---

# Andrew Macpherson
