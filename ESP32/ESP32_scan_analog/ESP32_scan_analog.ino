// List of ADC-capable pins on ESP32 (depends on the board)
// These are typical safe choices; adjust if your board has restrictions.
const int analogPins[] = { 0, 2, 4, 12, 13, 14, 15, 25, 26, 27, 32, 33, 34, 35, 36, 39 };
const int numPins = sizeof(analogPins) / sizeof(analogPins[0]);

// Array to store previous analog values
int lastValues[numPins];

// Sensitivity threshold
const int deltaThreshold = 100;

void setup() {
  Serial.begin(460800);
  delay(1000);
  Serial.println("Monitoring analog pins...");

  // Initialize lastValues with current readings
  for (int i = 0; i < numPins; i++) {
    lastValues[i] = analogRead(analogPins[i]);
  }
}

void loop() {
  delay(50);
  for (int i = 0; i < numPins; i++) {
    int pin = analogPins[i];
    int currentValue = analogRead(pin);
    if(pin == 34) {
      Serial.println(currentValue);
    }
    
    int delta = abs(currentValue - lastValues[i]);

    // if (delta > deltaThreshold) {
    //   Serial.print("Pin ");
    //   Serial.print(pin);
    //   Serial.print(" changed by ");
    //   Serial.print(delta);
    //   Serial.print(" (new value = ");
    //   Serial.print(currentValue);
    //   Serial.println(")");
      
    //   // Update last value
    //   lastValues[i] = currentValue;
    // }
  }

  delay(50); // Adjust as needed to control scan rate
}