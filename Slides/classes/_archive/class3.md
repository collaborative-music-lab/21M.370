# Modular Synthesis

Automatonism & PureData
---

<iframe data-autoplay src="https://www.youtube.com/embed/-IRs8Op2wuk?start=300" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

---

**Modular Synthesis**
- Sound sources: oscillators, samplers
- Modifiers: filters, amplifiers, FX
- Control signals: envelopes, LFOs
- Sequencers, clock generators

---

**PureData**
- visual programming language for music
- related to Max/MSP, Reaktor, and other music environments
- idiosyncratic, but we will basically ignore


**Automatonism**
- library built in Puredata
- super simple
- based on Eurorack modular concepts

---

## Puredata

<img src="https://patchstorage.com/wp-content/uploads/2024/01/Screenshot_2024-01-10_22-20-21-659f18405e49a.png" width="800" height="500" />

---
## Puredata

<div class="two-col">
  <div class="col-text">
  <strong>Essential:</strong>
  <ul>
    <li>Edit mode: allows for adding objects and connecting</li>
    <li>Filepath: PD ⇒ settings ⇒ path (will do later)</li>
    <li>Adding objects: in “Put” menu</li>
  </ul>
</div>

  <div class="col-image">
	<img src="./images/pd-edit-mode.png" class="medium-img"/>
  </div>
</div>

---

## Automatonism

<div class="two-col">
  <div class="col-text">
  <strong>Modules:</strong>
  <ul>
    <li>In on top, out on bottom</li>
    <li>Module parameters sliders are white</li>
    <li>Purple inputs are for control voltage</li>
    <li>Purple sliders attenuate CV input</li>
    <li>Red in/out is for sync/trigger</li>
  </ul>
</div>

  <div class="col-image">
	<img src="./images/pd-example-2.png" class="medium-img"/>
  </div>
</div>

---
<!-- .slide: data-background-image="./images/signal-flow.png"
             data-background-size="cover" -->

<div class="caption">
Sample signal flow in automatonism
</div>

---

<div class="two-col">
  <div class="col-text">
  <strong>Modules:</strong>
  <ul>
    <li>In on top, out on bottom</li>
    <li>Module parameters sliders are white</li>
    <li>Purple inputs are for control voltage</li>
    <li>Purple sliders attenuate CV input</li>
    <li>Red in/out is for sync/trigger</li>
  </ul>
</div>

  <div class="col-image">
	<img src="./images/pd-synth.png" class="medium-img"/>
  </div>
</div>

---
---
<img src="/images/pd-drums.png"
     style="width:600px; display:block; margin:0 auto;">

---



watch some videos
automatonism
automitonism
class github

automatonism basics
- adding modules
	- name and instance number
- maestro output
- pd setting audio output

module types
- outputs / mixers
- sound sources
	 - parameter names and ranges
	 	- we will address parameters with EXACTLY their name
	 	- instance numbers allows for targeting individual modules
	 - CV and CV inputs
	 - white sliders: standard parameter
	 - blue slider: CV attenutator
	 - green slider: bipolar CV attenuator
- control sources
- audio modifiers
- sequencers

