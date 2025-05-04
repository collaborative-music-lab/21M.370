#define AXP2101_ADDR 0x34
byte DEVICE_NUM = 1;
const char* DEVICE_NAME = "ESP";

#include "led.h"
#include "I2C_MPU6886.h"
#include "BLE.h"
#include "Display.h"
#include <Wire.h>

#include "Button.h"

#include <EEPROM.h>

#define EEPROM_SIZE 32
#define DEVICE_NUM_ADDR 0  // Where we'll store the device number

Button btnA(37);
Button btnB(39);

M5LCD lcd;

 byte SERIAL_DEBUG = 0;
 byte IMU_DEBUG = 0;
 byte IS_ACTIVE = 1;
 int imu_interval = 50;

m370_communication comms;

I2C_MPU6886 imu(I2C_MPU6886_DEFAULT_ADDRESS, Wire1);

LedBlinker led = {10, 500, 50}; 

//SETUP
void setup() {
  Wire1.begin(21, 22);
  Serial.begin(115200);

  btnA.begin();
  btnB.begin();
  pinMode(10, OUTPUT); //red led
  led.begin();

  loadDeviceNumberFromEEPROM();
  comms.startBLE();
  // comms.setCharacteristic(pCharacteristic);
  delay(100);

  init_AXP192();

  lcd.begin();
  lcd.fill(0xF800); // screen should go green now

  analogWrite(32,255); //max backlight brightness?

  imu.begin();
  led.set(100,50);
  delay(1000);
  Serial.printf("whoAmI() = 0x%02x\n", imu.whoAmI());

  Serial.println("M5 Stick C Plus setup complete");
  
}

//LOOP
void loop() {
  
  //if( !IS_ACTIVE ) return;
  readIMU();
  led.update();
  readButtons();

  //updateDisplay();
  monitorBattery();
}//loop

//READ FUNCTIONS

uint16_t readIMU(){
  uint32_t timer = 0;
  int sentBytes = 0;

  if(millis()-timer > imu_interval){
    timer = millis();
    float a[3];
    float g[3];
    float t;

    imu.getAccel(&a[0], &a[1], &a[2]);
    imu.getGyro(&g[0], &g[1], &g[2]);
    imu.getTemp(&t);

    //acc
    comms.outu8(71);
    for(int i=0;i<3;i++) comms.out16((int16_t)(a[i]*1000));
    comms.end();

    //gyro
    comms.outu8(72);
    for(int i=0;i<3;i++) comms.out16((int16_t)(g[i]*1000));
    comms.end();

    //temperature
    // comms.outu8(102);
    // comms.out16((int8_t)(t));
    // comms.end();
   sentBytes= comms.send();
    //Serial.println(comms.send());
  }
  return sentBytes;
}

uint16_t readButtons(){
  ButtonState a = btnA.update();
  ButtonState b = btnB.update();
  uint16_t sentBytes = 0;
  
  if (a == PRESSED) {
    Serial.println("A pressed");
    comms.outu8(10);
    comms.outu8(1);
    comms.end();
    sentBytes = comms.send();
  }
  if (a == RELEASED) {
    Serial.println("A released");
    comms.outu8(10);
    comms.outu8(0);
    comms.end();
    sentBytes = comms.send();
  }

  if (b == PRESSED) {
    Serial.println("B pressed");
    comms.outu8(11);
    comms.outu8(1);
    comms.end();
    sentBytes = comms.send();
  }
  if (b == RELEASED) {
    Serial.println("B released");
    comms.outu8(11);
    comms.outu8(0);
    comms.end();
    sentBytes = comms.send();
  }
  return sentBytes;
}



void updateDisplay(){
  static byte x = 0;
  static byte y = 0;
  //cd.fill(M5LCD::rgb(0, 0, 0)); // Clear to black
  lcd.drawPixel(x++, y++, M5LCD::rgb(255, 0, 0)); // Red pixel
}

void monitorBattery(){
  static uint32_t timer = 0;
  if(millis()-timer > 5000){
    timer = millis();
    float vbat = readBatteryVoltage();
    bool charging = isCharging();

    //lcd.fill(M5LCD::rgb(0, 0, 0)); // Clear screen

    char buf[32];
    sprintf(buf, "VBat: %.2f V", vbat);
    lcd.drawText(10, 10, buf, M5LCD::rgb(255, 255, 255));

    lcd.drawText(10, 30, charging ? "Charging" : "Not charging", M5LCD::rgb(255, 255, 0));
  }
}