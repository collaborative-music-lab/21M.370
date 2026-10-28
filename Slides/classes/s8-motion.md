
# Motion Data

21M.370 

Ian Hattwick

---

## Lab 7 

Assemble and test an IMU for in-class exploration
- motion sensing

---

## Performer Research

- What are their interests in terms of designing and performing with new instruments? What questions are they asking?
- How does their instrument work? What kinds of sensors, algorithms, software are they using?
- How does their performance practice incorporate their instrument?

Groups:
- November 16 [Imogen Heap](https://mimugloves.com)
- November 16 [Marco Donnarumma](https://marcodonnarumma.com)
- November 18 Lita - [Sonic Liberation Devices](https://sonicliberationdevices.com)
- November 18 [Chaoseflote - Melody Chua](https://thefluteview.com/2018/09/melody-chua-the-chaosflote/) 

---

# Imogen Heap

<iframe data-autoplay src="https://www.youtube.com/embed/ci-yB6EgVW4" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

---

# Marco Donnarumma

<iframe data-autoplay src="https://www.youtube.com/embed/CAIh8FxLMtk" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>


---

# DJLita

<iframe data-autoplay src="https://www.youtube.com/embed/pzz-rd0I76Q?t=5458" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

https://youtu.be/pzz-rd0I76Q?t=5458

---

# Melody Chua

<iframe data-autoplay src="https://www.youtube.com/embed/rgGhU9Yac3k" width="960" height="540" allow="autoplay; encrypted-media" allowfullscreen></iframe>

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
- or a BMI160!
- Uses I2C
- Mounts directly to our PCB!


---

## IMU Gestures

what hand gestures are useful with an imu? 
- tilt: pitch roll yaw (filter freq, timbre) 
- shaking to inject energy (maracas, percussion) 
- drum hit (in free air vs hitting a table)
- rotation 
- signal - gesture recognition ...


Challenges
- calculating velocity in triggers
- movement is slow, hard to segment fast passages
	- fast passages can just look like noise
- absolute perception
	- our subjective view and the IMUs view are often very different

---

## IMU Data

* Raw acceleration
* Raw angular velocity
* Tilt 
* Magnitude of acceleration
* Rotation angle
* Jerk

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

## Magnitude

Tracking the power of a signal
The ‘power’ of a signal is related to how much it has deviated from its base value. So we assume the base value is near 0.
* We can calculate the power of a signal over time by:
  1. capture a group of samples
  2. square all of the individual samples
  3. add them together
  4. take the root of the sum
  5. Also called the ‘root-mean-sum’ (RMS)

 ---

 ## Accelerometer magnitude

Power is a good way to describe the magnitude of an accelerometer:
1. square each axis of acceleration
2. add them together
3. take the square root
4. `magnitude = sqrt(ax^2 + ay^2 + az^2)`

---

# Change over time - derivative

The derivative is simply the change of value from one sample to the next.

The derivative, or delta, can be useful to detect sudden changes, e.g. plucks or strikes. There are several different kinds of derivatives we can take.
1. Given a single sensor data for the position of a sensor (for example an Mbira tine)
2. Velocity, first derivative: curPosition - prevPosition
3. Acceleration, second derivative: curVelocity - prevVelocity
4. Jerk, third derivative: curAccel - prevAccel
5. Snap, fourth derivative: curJerk - prevJerk

Raw accelerometer data is by definition acceleration. . . 

---

# Change over time - integration

Integration is adding together successive samples. 
- But this is often tricky as small errors will accumulate

- Acceleration
	- First integration: velocity
	- Second integration: position
- Angular velocity
	- First integration: angle

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

- Set a threshold and trigger hit immediately 
	- instantaneous value past trigger might not be peak acceleration
- Set a threshold and trigger hit on first negative acceleration value after threshold is passed 
	- may add latency 
	- allows for accurate magnitude detection
- Always need some way to prevent retriggers
	- Schmitt trigger?

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