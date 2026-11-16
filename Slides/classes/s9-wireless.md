
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

"The only thing worse that wires is wireless" - perry cook

The direct connection of gesture to sound is an essential part of DMIs. This is even true when you are working on a compositional level (sequencing, etc.). Predictability of response is crucial.

Most instruments work fine with wires. But sometimes wireless is unavoidable:
- dance-based instruments
- rotating instruments
- instruments distributed over long distances
- highly gesturally based instruments

---

# Limitations of wireless

- latency: added delay between sensors and sound generation
- jitter: inconsist intervals between sending data
- dropped packets: what happens when information is lost
- complexity
  - pairing: how to know where to send the information

---

## Types of wireless

- WiFi: high bandwidth, poor latency and jitter
- Standard Bluetooth: flaky, poor latency
- Bluetooth LE: needs special pairing code
- ESP-NOW: only works with ESP devices
- LoRa: needs special hardware

---

## What could possibly go wrong?

Potential problems vary depending on the kind of data you are sending:
- events(note on/off, start/stop messages):
  - missed messages are destructive!
  - every message is critical
- cc messages (stream data as you are changing the value)
  - only sends data when it changes
  - missing the last few packets can lead to an incorrect value
- streaming data (IMUs)
  - sends lot of data, hogs up bandwidth
  - filters depend on consistent data
  - missed packets cause problems

---

## Preventing problems

Confirming packets are received
- most protocols already support packet acknowledgement
- but sometimes this blocks processing!
- ack packets add latency, complexity
- sending data to lots of receivers means lots of ack packets!

Confirming a steady stream for streaming data
- missed information is less important (new data is always about to come)
- but filters that process based on incoming data can be a problem!
- in the receiver, have a way of recognizing missed packets, and substituting old data instead