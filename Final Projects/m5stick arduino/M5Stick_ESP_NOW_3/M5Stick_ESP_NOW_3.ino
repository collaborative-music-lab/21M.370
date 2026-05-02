/*
This firmware is designed to stream data from an M5Stick CPlus over ESP-NOW.
- this will be loaded on the m5stick itself.

ESP-NOW is a proprietary radio protocol developed by the creators of the ESP32.
It is much lower overhead and latency than Bluetooth or Wi-Fi.
It requires both a transmitter and a receiver based on a ESP32.

This version attempts to use the built-in M5stick library in Arduino

*/

#define AXP2101_ADDR 0x34
#define ESPNOW_WIFI_CHANNEL 2
#define SERIAL_DEBUG 1
#define IMU_DEBUG 0
#define IS_ACTIVE 1
#define imu_interval 50

#include <M5StickCPlus.h>
#include "led.h"
#include "I2C_MPU6886.h"
#include <Wire.h>

#include "ESP32_NOW.h"
#include "WiFi.h"

#include <esp_mac.h>  // For the MAC2STR and MACSTR macros

// Define the structure
struct __attribute__((packed)) ImuPacket {
    char header[4]; // "imu" + null terminator (or just 3 bytes if you prefer)
    float a[3];     // ax, ay, az
    float g[3];     // gx, gy, gz
    uint8_t number;
};
ImuPacket packet;

/* Classes */
// Creating a new class that inherits from the ESP_NOW_Peer class is required.
class ESP_NOW_Broadcast_Peer : public ESP_NOW_Peer {
public:
  // Constructor of the class using the broadcast address
  ESP_NOW_Broadcast_Peer(uint8_t channel, wifi_interface_t iface, const uint8_t *lmk) : ESP_NOW_Peer(ESP_NOW.BROADCAST_ADDR, channel, iface, lmk) {}
  // Destructor of the class
  ~ESP_NOW_Broadcast_Peer() {
    remove();
  }
  // Function to properly initialize the ESP-NOW and register the broadcast peer
  bool begin() {
    if (!ESP_NOW.begin() || !add()) {
      log_e("Failed to initialize ESP-NOW or register the broadcast peer");
      return false;
    }
    return true;
  }
  // Function to send a message to all devices within the network
  bool send_message(const uint8_t *data, size_t len) {
    packet.number += 1;
    if (!send(data, len)) {
      log_e("Failed to broadcast message");
      return false;
    }
    return true;
  }
};

/* Global Variables */
uint32_t msg_count = 0;
// Create a broadcast peer object
ESP_NOW_Broadcast_Peer broadcast_peer(ESPNOW_WIFI_CHANNEL, WIFI_IF_STA, nullptr);

I2C_MPU6886 imu(I2C_MPU6886_DEFAULT_ADDRESS, Wire1);


//SETUP
void setup() {
  Wire1.begin(21, 22);
  Serial.begin(115200);

  M5.begin();
  M5.Lcd.setRotation(3);

  // Initialize the Wi-Fi module
  WiFi.mode(WIFI_STA);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL);
  while (!WiFi.STA.started()) {
    delay(100);
  }

  Serial.println("Wi-Fi parameters:");
  Serial.println("  Mode: STA");
  Serial.println("  MAC Address: " + WiFi.macAddress());
  Serial.printf("  Channel: %d\n", ESPNOW_WIFI_CHANNEL);

  // Register the broadcast peer
  if (!broadcast_peer.begin()) {
    Serial.println("Failed to initialize broadcast peer");
    Serial.println("Reebooting in 5 seconds...");
    delay(5000);
    ESP.restart();
  }

  Serial.printf("ESP-NOW version: %d, max data length: %d\n", ESP_NOW.getVersion(), ESP_NOW.getMaxDataLen());

  pinMode(10, OUTPUT); //red led
  // led.begin();

  delay(100);

  init_AXP192();

  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(10, 10);
  M5.Lcd.printf("MY MAC:\n");
  M5.Lcd.setCursor(10, 40);
  M5.Lcd.printf("%s \n", WiFi.macAddress().c_str());
  M5.Lcd.setCursor(10, 70);
  M5.Lcd.printf("ESP-NOW Channel: %d \n", ESPNOW_WIFI_CHANNEL);

//   lcd.begin();
//   lcd.fill(0xF800); // screen should go green now
//   // 1. Create a buffer large enough for your text
// char macBuffer[32]; 

// // 2. Format the string into the buffer (instead of printing it to serial)
// snprintf(macBuffer, sizeof(macBuffer), "MY MAC: %s", WiFi.macAddress().c_str());

// // 3. Pass the buffer to your draw function
// lcd.drawText(10, 10, macBuffer, 100);

  // analogWrite(32,255); //max backlight brightness?

  imu.begin();
  strncpy(packet.header, "imu", 4); // Set the prefix
  packet.number = 0;
  Serial.println("M5 Stick C Plus setup complete");
  Serial.println("Setup complete.");
}

//LOOP
void loop() {

  //if( !IS_ACTIVE ) return;
  readIMU();
  // led.update();
  // readButtons();

  //updateDisplay();
  // monitorBattery();
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

    if(SERIAL_DEBUG){
      for(int i=0;i<3;i++) {
        Serial.print((int16_t)(a[i]*1000));
        Serial.print("\t");
      }
      Serial.println();
      //return 3;
    }

    // Fill the arrays (assuming your arrays are named 'a' and 'g')
    for(int i=0; i<3; i++) {
        packet.a[i] = a[i];
        packet.g[i] = g[i];
    }

    // Send the entire struct as a byte array
    broadcast_peer.send_message((uint8_t *)&packet, sizeof(packet));

    M5.Lcd.setCursor(10, 100);
    M5.Lcd.printf("Sent: %.2f, %.2f",a[0], a[1]);
    
  }
  return sentBytes;
}


void monitorBattery(){
  static uint32_t timer = 0;
  if(millis()-timer > 5000){
    timer = millis();
    float vbat = readBatteryVoltage();
    bool charging = isCharging();

    //lcd.fill(M5LCD::rgb(0, 0, 0)); // Clear screen

    char buf[32];
    // sprintf(buf, "VBat: %.2f V", vbat);
    // lcd.drawText(10, 10, buf, M5LCD::rgb(255, 255, 255));

    // lcd.drawText(10, 30, charging ? "Charging" : "Not charging", M5LCD::rgb(255, 255, 0));
  }
}