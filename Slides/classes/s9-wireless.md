
# Wired vs Wireless

21M.370 

Ian Hattwick

---

## Upcoming 

* in class performances
* performer research
* final project progress report

---

## Final Project Progress Report

Your artist statement should talk about WHY you are making your instrument. This should tie the performance experience and physical manifestation of the instrument to the sound design and compositional elements of the piece you are planning on performing with it.

One way to start is to talk about an inspiration

* musical inspiration
* performing with an existing instrument
* a performance experience (concert, artwork, sound walk, etc.)
* a philosophical or conceptual idea

Once you have identified an inspiration, talk about how specifically it relates to the instrument you are building. Be as specific as you can - it might be a weak or tenuous connection, but it is important to be able to articulate anyway.

---

# Why wired vs wireless

> "The only thing worse than wires is wireless." - Perry Cook

In a digital musical instrument (DMI), the direct connection between gesture and sound is essential. This holds at the compositional level too, such as sequencing and arrangement, where predictability matters as much as immediacy. A sensor that responds late, jitters, or drops out breaks the performer's sense of control.

- Dance-based instruments, where cables restrict movement or snag on the performer
- Rotating instruments, where a cable would wrap or require slip rings
- Distributed instruments, spread across a stage, room, or venue, or over longer distances
- Highly gestural instruments, where cable weight or tension alters the movement being sensed

---

# Limitations of Wireless

- Latency: Added delay between sensing a gesture and producing sound. 
- Jitter: Variation in the timing between packets. Data may arrive at uneven intervals (for example, 10 ms, 14 ms, 8 ms) rather than as a steady stream.
- Packet loss: Data that never arrives. 
- Complexity:
  - Pairing: How the sensor and receiver find each other and agree on where data should go. 
  - Configuration: What options are there for avoiding interference?
  - Reliability in performance: Performance venues with large audiences soak up RF waves, and also add a lots of RF noise with lots of mobile devices.

---

# Types of Wireless

**WiFi**: High bandwidth, with variable latency and jitter.
- Good for sending large amounts of data.
- Lots of jitter due to other traffic and power-saving behavior
- A dedicated router, with few other devices on the network, reduces interference and jitter

**Classic Bluetooth** (BR/EDR): Generally not recommended for real-time control.
- Latency is typically tens of milliseconds and inconsistent.
- The OS handles pairing, and the link often appears as a virtual serial port (a COM port on Windows, `/dev/tty*` on macOS and Linux).

**LoRa**: Long-range, low-bandwidth radio.
- Very low data rate and long packet airtime make it unsuitable for high-rate sensor streams.

---

# Types of Wireless

**Bluetooth LE**: Good for small, frequent packets.
- Latency depends on the connection interval, minimum 7.5 ms but often longer.
- Default packet size of **20 bytes**!
- Pairing is optional. Pairing is used for security.
- Laptops support BLE natively. BLE MIDI is a standard that works without extra hardware.

**ESP-NOW**: (or other proprietary protols)
- A simple, low-overhead protocol for ESP32-family devices.
- Packets are small (about 250 bytes).
- Devices pair by MAC address, or you can send broadcast packets to all nearby devices.
- Requires ESP devices at both ends.
- Typically low and predictable latency and jitter.

---

## Summary Table

| Protocol | Typical use | Latency/jitter | Laptop support | Data rate |
|---|---|---|---|---|
| WiFi (UDP) | Many sensors, high bandwidth | Variable | Native | High |
| Classic Bluetooth | Serial link | Tens of ms, inconsistent | Native (serial port) | Moderate |
| BLE | Small, frequent packets | Low, depends on interval | Native (with BLE MIDI or custom code) | Low to moderate |
| ESP-NOW | Device-to-device, ESP32 | Low, predictable | Needs ESP32 bridge | Low to moderate |
| LoRa | Long range, low rate | Long airtime | Needs hardware | Very low |


---

## What could possibly go wrong? (Events)

Potential problems vary depending on the kind of data you are sending:

#### Events (note on/off, start/stop)

- Lost messages are serious. A lost note-on or note-off can leave a note stuck, or a sequence that never starts or stops.
- Latency is noticeable but learnable. A small constant delay can be compensated for, and performers adapt to it. Latency more than 50ms is really hard to work with though.
- Jitter is more damaging than latency. Unpredictable timing prevents you from accommodating latency - and will also affect the groove in noticeable ways.

---

## What could possibly go wrong? (ccs)

#### Control changes (CC)

- Data is sent only when the value changes. Between messages, the receiver holds the last value it received.
- Losing the final packet leaves the receiver wrong. If the last update in a gesture is dropped, the synth stays at an incorrect value until the next change.
- Mitigations:
  - Resend the current value periodically, for example every 100 to 500 ms, so a lost update is corrected quickly.
  - Rate-limit the sender to reduce traffic, which also reduces the chance of loss.

---

## What could possibly go wrong? (Streaming Data)

- Data rate is steady and can be high. A 6-DoF IMU at 100 Hz with 16-bit values produces about 1.2 kB/s. The more data there is, the higher probability of dropped packets or jitter!
- Filters assume regular input. Filters expect input at a fixed interval. If a filter update is skipped due to a missed packet it will change the filter's frequency.
- Missed packets create inconsistencies. Lots of packet loss can cause the data to feel 'jumpy'.

---

## You Can't Prevent Errors, So Design for Them

Every wireless link will drop, delay, or reorder data eventually. How we will deal with this depends on what we are sending:

* Events: make sure they arrive, or have a fallback plan
* CCs: resend periodically to make sure constant values are correct.
* Streaming: maintain a steady data stream at the *receiver*.

---

## Events: Make Sure They Arrive

All protocols already use packet acknowledgement at the hardware level for preventing packet drops:
* The transmitter (TX) sends a message to the receiver (RX).
* RX sends an ACK anknowledgement message back to TX.
* If TX does not receive an ACK message it resends the packet.
* After a certain amount of time or resends the TX stops resending.

This process can add significant jitter or other problems - you can often configure the timeout if you want to.

#### Higher level ACKs

You can also handle dropped packets in your own code, or just in higher level protocols. TCP, for example, has more robust retransmission than UDP. But TCP also has much higher latency and jitter because of this.
* Don't use TCP!

---

## Solving packet drops

* Use a packet number (just an incrementing integer) to detect packet drops. 
  * A gap in the packet numbers indicate a dropped packet.
  * Have RX ask for packets it did not receive.
* Send a collection of states
  * If you have 8 buttons, send all 8 values every time one changes state.
  * For MIDI notes, send an array of the state of the 8 most recently played notes.
* Resend events manually
  * Send each packet multiple times manually
    * Especially useful for note-offs
  * Or send a messages (for starting or stopping sequences, for exmaple) repeatedly every second.

Note-on messages are very timing sensitive: maybe send multiple times quickly (fastest possible speed)?
Note-off messages are less timing sensitive, but very annoying when missed: maybe send several times at 100ms intervals?

---

## Accommodating lost data from streams

My favourite way of handling this is to have the *RX* have its own internal clock driving data being sent to filters or other continuous processes.
* The receiver sets its clock at a frequency, e.g. 100Hz.
* A variable (e.g. `sensorData`) in the receiver stores the most recent sensor value.
* Every time the receiver's clock fires `sensorData` is passed to the filter.
* When a new value is received from the TX it is stored in `sensorData`.

This works best when you know the TX transmission rate and set the RX clock to match.

---

## Advice for working with wireless systems

* Choose the right method.
  * We will use ESP-NOW and BLE.
* Send only the data you need.
  * Send raw bytes, not ASCII or strings.
  * Send smaller data types, e.g. 8- or 16-bit instead of 32
  * Only send data as fast as you need.
* Sends batches of data
  * Sending small packets adds more overhead due to headers.
  * If you have different kinds of sensors, consider a single fixed data rate and package all of the data together. 
  * But be aware of the total packet size!

---

## Advice for working with wireless systems

* Minimize the distance between TX and RX
  * Shorter distances and clear line of sight give the most reliable links.
  * Performance environments change quickly. Crowds, bodies, and metal structures all absorb or reflect 2.4 GHz energy, so test in the actual space.
* Use external antennas when you can
  * Use a board with an external antenna connector, or a well-placed PCB antenna clear of metal and performers' bodies.
  * Higher-power transmitters and bigger antennas can improve reliability
  * Use commercially available tech when it makes sense


