void init_AXP192() {
  // Enable ADC for battery voltage (Vbat)
  Wire1.beginTransmission(0x34);
  Wire1.write(0x82);  // ADC enable 1
  Wire1.write(0xFF);  // Enable all ADCs
  Wire1.endTransmission();

  Wire1.beginTransmission(0x34);
  Wire1.write(0x83);  // ADC enable 2
  Wire1.write(0xFF);
  Wire1.endTransmission();

  // Set LDO2 voltage to 3.0V (used for LCD backlight)
  Wire1.beginTransmission(0x34);
  Wire1.write(0x28);     // LDO2/3 voltage config
  Wire1.write(0xCC);     // 0xCC = ~3.0V
  Wire1.endTransmission();

  // Enable LDO2 output (bit 2 of reg 0x12)
  Wire1.beginTransmission(0x34);
  Wire1.write(0x12);     // Power output control register
  Wire1.endTransmission(false);
  Wire1.requestFrom(0x34, 1);
  uint8_t pwr = Wire1.read();

  pwr |= (1 << 2);       // Enable LDO2
  Wire1.beginTransmission(0x34);
  Wire1.write(0x12);
  Wire1.write(pwr);
  Wire1.endTransmission();

  Serial.println("AXP192 init");
}//initAXP192

float readBatteryVoltage() {
  Wire1.beginTransmission(0x34);
  Wire1.write(0x78);  // Battery voltage high byte
  Wire1.endTransmission(false);
  Wire1.requestFrom(0x34, 2);

  if (Wire1.available() < 2) return -1.0;
  uint16_t raw = (Wire1.read() << 4) | (Wire1.read() & 0x0F);
  return raw * 1.1 / 1000.0;  // Scale per datasheet
}

bool isCharging() {
  Wire1.beginTransmission(AXP2101_ADDR);
  Wire1.write(0x20); // Power mode register
  if (Wire1.endTransmission(false) != 0) {
    Serial.println("AXP2101: Charging status read failed");
    return false;
  }

  Wire1.requestFrom(AXP2101_ADDR, 1);
  if (!Wire1.available()) {
    Serial.println("AXP2101: No bytes for charging status");
    return false;
  }

  uint8_t status = Wire1.read();
  return status & 0x08; // Bit 3 = charging
}

//EEPROM

void loadDeviceNumberFromEEPROM() {
  EEPROM.begin(EEPROM_SIZE);
  uint8_t stored = EEPROM.read(DEVICE_NUM_ADDR);
  if (stored >= 1 && stored <= 99) {
    DEVICE_NUM = stored;
  } else {
    DEVICE_NUM = 1;
  }
}

void saveDeviceNumberToEEPROM(int num) {
  EEPROM.write(DEVICE_NUM_ADDR, num);
  EEPROM.commit();
}
