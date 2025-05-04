#pragma once
#include <Arduino.h>

enum ButtonState {
  UP,
  DOWN,
  PRESSED,
  RELEASED
};

class Button {
public:
  Button(uint8_t pin, bool activeLow = true)
    : _pin(pin), _activeLow(activeLow), _state(UP),
      _lastRaw(false), _lastDebounced(false),
      _lastChangeTime(0), _debounceDelay(20) {}

  void begin() {
    pinMode(_pin, _activeLow ? INPUT_PULLUP : INPUT);
  }

  ButtonState update() {
    bool raw = digitalRead(_pin);
    if (_activeLow) raw = !raw;  // invert if active-low

    unsigned long now = millis();

    if (raw != _lastRaw) {
      _lastChangeTime = now;
      _lastRaw = raw;
    }

    if ((now - _lastChangeTime) >= _debounceDelay) {
      if (raw != _lastDebounced) {
        _lastDebounced = raw;
        _state = raw ? PRESSED : RELEASED;
      } else {
        _state = raw ? DOWN : UP;
      }
    } else {
      _state = _lastDebounced ? DOWN : UP;
    }

    return _state;
  }

private:
  uint8_t _pin;
  bool _activeLow;

  ButtonState _state;
  bool _lastRaw;
  bool _lastDebounced;
  unsigned long _lastChangeTime;
  const uint8_t _debounceDelay;
};