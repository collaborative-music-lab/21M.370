
struct LedBlinker {
  uint8_t pin;
  uint32_t period;     // total cycle time in ms
  uint8_t duty;        // % ON time (0–100)

  // Internal state
  bool state = false;           // current pin state
  uint32_t lastToggle = 0;      // timestamp of last change

  void begin() {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
    state = false;
    lastToggle = millis();
  }

  void update() {
    uint32_t now = millis();
    uint32_t onTime = (period * duty) / 100;
    uint32_t offTime = period - onTime;

    if (duty == 0) {
      digitalWrite(pin, LOW);
      return;
    } else if (duty == 100) {
      digitalWrite(pin, HIGH);
      return;
    }

    if (state && now - lastToggle >= onTime) {
      digitalWrite(pin, LOW);
      state = false;
      lastToggle = now;
    } else if (!state && now - lastToggle >= offTime) {
      digitalWrite(pin, HIGH);
      state = true;
      lastToggle = now;
    }
  }

  void set(uint32_t newPeriod, uint8_t newDuty) {
    period = max(10UL, newPeriod);  // clamp to avoid 0
    duty = constrain(100-newDuty, 0, 100);
  }
};//led struct