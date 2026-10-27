
# Gestures and Sensors

21M.370 

Digital Instrument Design

Ian Hattwick

---

## Gesture

1. Intentional body motion
2. Sonic change over time
3. Physical reaction to sound
4. Semantic communication

Body motion and sound - Godøy

---

# Sensors
   1. How to turn gestural action into digital data
   2. Generally NOT directly tied to gesture
   3. How can we use sensors to gather data about gestural actions?
---

# Components of a gesture/sensor interaction

   1. Intentionality
   2. Physical action
   3. Mechanical motion
   4. Transduction of movement into data
      1. Analog (voltage)
      2. digital 

---


# Case study: potentiometer
   1. Intend to change volume
   2. Touch knob and turn
   3. Physical rotation of knob and wiper
   4. Transduction of wiper position to voltage change

---

# Case study: keyboard press

1. Intend to play a note
2. Touch key and press
3. physical motion of key changes and triggers two buttons
4. final button triggers note event
5. time delta between button presses turn to velocity
6. Alternate: Force Sensing Resistor (FSR)
7. linnstrument: https://youtu.be/MDTikW1BFt8?t=39

---

<iframe data-autoplay src="https://www.youtube.com/embed/MDTikW1BFt8" width="1720" height="880" allow="autoplay; encrypted-media" allowfullscreen></iframe>


https://youtu.be/MDTikW1BFt8?t=39


---

# Case study: The Hands squeeze motion

1. Intend to control volume
2. Move ultrasound sensors to opposing positions, and move hands
3. Distance between ultrasound sensors changes
4. Time between pings converted to voltage by ultrasound sensor
5. Alternate: Time of Flight (ToF) sensor
6. Pamela Z: [Pamela Z](https://youtu.be/ebxvVJwGWek?t=149)

---

<iframe data-autoplay src="https://www.youtube.com/embed/ebxvVJwGWek" width="1720" height="880" allow="autoplay; encrypted-media" allowfullscreen></iframe>

time 149


---

# Case study: Capacit interaction

1. Intend to fade in note
2. Move hands towards sensor
3. Distance between hand and touchpad changes
4. Capacitance is measured and converted to a digital signal
5. Alternate: Jeff Snyder Manta: https://youtu.be/O_GLWIITiGo

---

<iframe data-autoplay src="https://www.youtube.com/embed/O_GLWIITiGo" width="1720" height="880" allow="autoplay; encrypted-media" allowfullscreen></iframe>


---

# Case study: Haken Continuum

1. Intend to initiate note
2. Press down on surface
3. Aluminum bars depress
4. Position of bar ends is converted to voltage via hall effect sensors
5. [ContinuuCon](https://www.youtube.com/watch?v=SiAb48qsZHY&t=1077s)
6. Alternative: TMR (Tunnel Magnetoresistance) sensors (ask Evan)

---

<iframe data-autoplay src="https://www.youtube.com/embed/SiAb48qsZHY" width="1720" height="880" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Time 0:1077


---

# Case study: Monome Arc

1. Intend to speed up sequence
2. Twist knob
3. Encoder knob turns, triggering sequential patterns in encoder contacts
4. Pattern of contacts are decoded into information on rotation movement
5. Monome Arc https://www.youtube.com/watch?v=HM0EBvJe1s0, time 0:56

---

<iframe data-autoplay src="https://www.youtube.com/embed/HM0EBvJe1s0" width="1720" height="880" allow="autoplay; encrypted-media" allowfullscreen></iframe>

