
# Sensors III

21M.370 

IMUs, Encoders, and Photocells - oh my!

Ian Hattwick

---

## Lab 8 

Assemble and test an IMU for in-class exploration
- motion sensing
- machine learning

Also includes info on assembling other sensors:
- lever switches
- encoders
- photocells
- hall effect sensors

---

## Performer Research

- What are their interests in terms of designing and performing with new instruments? What questions are they asking?
- How does their instrument work? What kinds of sensors, algorithms, software are they using?
- How does their performance practice incorporate their instrument?

Groups:
- April 13 Chagall
- April 15 Jeff Snyder and Manta
- April 22a Mari Kimura
- April 22b Onyx Ashanti - Node 0

---

# Chagall

<iframe data-autoplay src="https://www.youtube.com/embed/2ahP8lPwIKs?start=61" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

---

# Jeff Snyder

<iframe data-autoplay src="https://www.youtube.com/embed/7YMYPuDfGJk?start=770" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>


---

# Mari Kimura

<iframe data-autoplay src="https://www.youtube.com/embed/hnEJNhPRhYg?start=40" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

---

# Onyx Ashanti

<iframe data-autoplay src="https://www.youtube.com/embed/LZ6NR6T-67M" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

---

# Sensors

---

## limit switches

<div class="image-wrapper">
<img src="./images/limit-switch.jpeg" class="medium-img"/>
</div>

Extremely light action
Comes in a variety of sizes
- we had a bunch of one size, with breakout PCBs for mounting
- great for finger switches!

---

## limit switches

Chester!

<div class="image-wrapper">
<img src="./images/chester_01.jpg" class="large-img"/>
</div>

Chester!

---

## rotary encoders

<div class="image-wrapper">
<img src="./images/encoder.png" class="small-img"/>
</div>

Measures rotational steps
- contains two switches with contacts with staggered phases
- interpretation of change of phases over time indicates direction of movement
- 'quadrature encoding'
- switches will bounce just like all switches
- super important to limit bounces! best to do it before the ADC

---

## encoders

<div class="image-wrapper">
<img src="https://ccrma.stanford.edu/workshops/mid2005/sensors/quadrature.png" class="large-img"/>
</div>

<div class="image-wrapper">
<img src="https://ccrma.stanford.edu/workshops/mid2005/sensors/encoder_filter.png" class="medium-img"/>
</div>


Source:
https://ccrma.stanford.edu/workshops/mid2005/sensors/encoder.html

---

## photocells

<div class="image-wrapper">
<img src="./images/photocell1.jpeg" class="medium-img"/>
</div>
<div class="image-wrapper">
<img src="./images/photocell2.jpeg" class="medium-img"/>
</div>

---

## hall effect switches

<div class="image-wrapper">
<img src="https://mm.digikey.com/Volume0/opasdata/d220001/derivates/1/100/954/264/296_TO-92-3_sml.jpg" class="medium-img"/>
</div>


---

## Inertial Measurement Units

Accelerometers
- Acceleration (not velocity)
- includes 1G of gravity!
- gravity is useful, allows for measurement of static tilt

Gyroscopes
- rotation (not angle!)
- super responsive!

Magnetometers
- direction to magnetic north
- slow, prone to interference

---

## Degrees of freedom

6/9 DoF sensors
- degrees of freedom - independent measurement. XYZ = 3 degrees
- 6 DoF typically means XYZ accel and XYZ gyro
- 9 DoF includes magnetometer
- 9 DoF also sometimes referred to as MARG sensors (Magnetic, Angular Rate, and Gravity)

<div class="image-wrapper">
  <img src="./images/degrees-of-freedom.png" 
       class="large-img" 
       style="transform: rotate(270deg);
       height: 500px; width: auto;" 
       />
</div>


---

## LSM6DS3

<div class="image-wrapper">
  <img src="https://pmdway.com/cdn/shop/products/LSM6DS3-6-dof-pmdway-4_739x412.jpg?v=1611721002" 
       class="large-img" 
       style="transform: rotate(0deg);" />
</div>

We will use a 6 DoF LSM6DS3 IMU.
- Uses I2C like MPR121
- Mounts directly to our PCB!


---

## IMU Gestures

what hand gestures are useful with an imu? 
- tilt: pitch roll yaw (filter freq, timbre) 
- shaking to inject energy (maracas, percussion) 
- drum hit (in free air vs hitting a table)
- rotation 
- signal - gesture recognition 


Challenges
- velocity? 
- slow, hard to segment fast passages 
- absolute perception, perception in our sense is hard 


---

## Tilt

Tilt is the most common usage of accelerometer data. 
- It is easy to make sense of, physically 
- It provides a static value which is easy to map
Accelerometer will always register gravity 
- gravity is a strong force!

<div class="image-wrapper">
<img src="./images/tilt-axes.png" class="large-img"/>
</div>

---

## Tilt

Naive: x=roll, y=pitch 
- axes are interactive and x acceleration doesn’t map linearly to roll angle
The best way to calculate tilt is: 
pitch = arctan(-accelX, sqrt(accelY² + accelZ²)) 
roll = arctan(accelY, sqrt(accelX² + accelZ²))

Yaw can't be accurately calculated using accelerometer - no change in static G force!
 
 
---

## Rotation

Absolute angle needs a fixed reference 
- for pitch and roll, gravity provides the reference 
- for gyro based yaw, we need to provide that reference explicitly
Naive: yaw += gyroZ 
- will drift badly 
- often a trigger is used to redefine 0 degrees yaw

---

## Triggers

‘Air Drums’ 
- at what point is a drum struck? 
- not interested in specific angles, but overall acceleration
Magnitude of acceleration: calculates total acceleration independent of axes 
- magnitude = sqrt(x^2 + y^2 + x^2) 
- subtract the static gravity value


---

## Detecting a trigger

Set a threshold and trigger hit immediately 
- instantaneous value past trigger might not be peak acceleration
Set a threshold and trigger hit on first negative acceleration value after threshold is passed 
- may add latency 
- allows for accurate magnitude detection
Always need some way to prevent retriggers

---

## Shaking

Overall running average of magnitude  
- easy to calculate 
- neatly correlates to physical activity
Calculation: 
- lowpass filter 
- leaky integrator: continuously integrate magnitude, add constant leak to bring value back to 0 
- shake = (mag + shake * leak) 
- shake = mag + shake - leak


