# What is Modular Synthesis

- **Modularity Concept**: A synthesizer built from individual functional units (modules) that can be connected in any order to create unique sounds.
- **Patch Cables**: Physical cables that route audio and control signals between modules, allowing you to create custom signal flows.
- **Flexibility vs Simplicity**: Modular systems offer unlimited creative possibilities but require understanding how signals flow and modules interact.
- **Analog programming?**: Very similar to early computing concepts, and also directly applicable to digital signal processing on computers

---

# History and Types of Modular Synthesis

- **Early Synthesizers (1960s)**: Moog and Buchla developed the first modular synthesizers as room-sized installations with patch cables.
- **Buchla vs Moog Philosophy**: Buchla focused on control and randomization for experimental music, while Moog emphasized intuitive sound design for performance.
- **Eurorack Format (1990s)**: A standardized rack size that focused on smaller sizes, and lower prices. Create by Doepfer, who still make Eurorack modules.
- **Visual programming?**: Programs like Max/MSP, Pure Data, and others draw on the modular concept to make full programming environements. Any software environment that focuses on *signal flow* might use a visual modular interace. 
- **Why do people like it?**
	- A combination of hands-on control, clearly visible signal flow, and easy configurability
	- Easy creative exploration, no *need* to have a clear mental model just to explore possibilities
	- The ability to design your own custom system
	- The tension between simple modules, vs complex and deep modules
	- The ability to go beyond conventional approaches to synthesis

---

# Software modular synthesis

- **Software modulars** 
	- VCV Rack
	- Reaktor
	- Nord Modular
	- Automatonism
- **Why Automatonism?**
	- Combination of PD (flexible programming) and modular (well-defined modules)
	- Easy(!) routing of control signals to modules (and to sends!)
	- Ability to easily share files that work the same across computers
	- No accounts to login, no cloud stuff, no subscription fees, etc.
	- Portable to microcontrollers, VST plugings, Web sites, many other places
	- Fully open source!

---

# Audio and Control Signals

- **Audio Rate Signals**: High-frequency signals (audible frequencies, typically 20Hz-20kHz) that contain the actual sound you hear from speakers.
- **Control Rate Signals (CV)**: Slower signals (often under 20Hz) that modulate parameters of other modules like pitch, filter cutoff, or amplitude.
- **Voltage Representation**: Both signal types are represented as voltages in hardware modular systems, typically ranging from -5V to +5V or 0V to +10V.
	- in automatonism signals audio signals are -1 to 1, and control signals are 0 to 1
- **Interchangeability**: Audio and control signals use the same patch cables, so you can use audio-rate signals as modulation sources for creative effects.
- **Polyphonic vs Monophonic**: Most modular systems are monophonic (one voice)
	- We will see how to make polyphonic synths easily in a little bit

---

# Sound Sources

- **Oscillators (VCOs)**: Modules that generate periodic waveforms (sine, square, sawtooth, triangle) at a frequency controlled by pitch CV.
- **Waveform Selection**: Different waveforms have different harmonic content (sine is pure, sawtooth is bright, square is hollow) for varied sonic character.
- **Pulse Width Modulation**: Varying the width of a square wave creates evolving timbral changes useful for dynamic, living sounds.
- **Noise Generators**: Modules that produce white, pink, or colored noise useful for percussion, texture, and as modulation sources.
- **FM Synthesis**: Frequency modulating one oscillator with another creates complex, bell-like and metallic tones used in classic synthesis.

---

# Filters

- **Voltage Controlled Filter (VCF)**: A module that removes or emphasizes frequencies based on a cutoff frequency controlled by CV signals.
- **Filter Types**: Lowpass (removes high frequencies), highpass (removes low frequencies), bandpass (isolates a frequency range), and notch (removes a specific frequency).
- **Resonance/Q**: Emphasizes frequencies at the cutoff point, creating a peak in the response that can self-oscillate and produce sine tones.
- **Filter Slope**: Measured in dB/octave (typically 12dB or 24dB), steeper slopes create more dramatic filtering and tonal changes.
- **Envelope Modulation**: Connecting an envelope to the filter cutoff creates classic "sweeping" filter effects essential to subtractive synthesis.
- **Drive and Saturation**: Many filters include distortion that adds harmonic richness and aggression to the filtered sound.
	- The different filters in automatonism have different characteristics, including distortion. 

---

# Envelopes

- **Attack-Decay-Sustain-Release (ADSR)**: A standard envelope shape controlling how a sound's amplitude evolves from trigger to release.
- **Attack**: The time it takes for the sound to rise from silence to peak volume after receiving a trigger signal.
- **Decay**: The time for the sound to fall from peak to the sustain level after the attack phase completes.
- **Sustain**: The held amplitude level while a gate signal is active, remaining constant until the key is released.
- **Release**: The time it takes for the sound to fade to silence after the gate signal ends, creating the tail of the note.
- **Modulation Destinations**: Envelopes can be routed to control:
	- VCA level (amplitude)
	- filter cutoff (frequency) 
	- VCO pitch 
	- any other parameter

---

# Triggers and Gates

- **Gate Signal**: A voltage signal that turns on (high) or off (low)
	- Generally a discrete control triggers on or off
	- e.g. a keyboard press 
	- typically used to for ADSR envelopes
- **Gate Length**: The duration a gate remains "on" affects the sustain phase of an envelope and overall note length
- **Trigger Signal**: A brief pulse
	- Goes on-off very quickly
	- Used for simple decay envelopes, to trigger a clock, etc.

---

# VCAs and Controlling Volume

- **Voltage Controlled Amplifier (VCA)**: A module that adjusts the amplitude of an audio signal based on a control voltage input.
- **In PD**: a `*~` object is a simple VCA, where the right inlet is the CV inlet.
- **Envelope Control**: Connecting an envelope to a VCA's CV input creates amplitude shaping, making sounds attack and decay naturally.
- **Output Mixing**: Multiple audio sources can be sent to a summing mixer or cascaded through VCAs to blend and control the final output level.
- **Depth and Attenuation**: VCA inputs typically include attenuators to scale how much the control voltage affects the audio signal's amplitude.
- **Daisy-Chaining**: Multiple VCAs can be stacked to control independent parameters or create complex rhythmic patterns through multiple modulation layers.