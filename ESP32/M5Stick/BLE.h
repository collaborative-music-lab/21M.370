#include "lwip/arch.h"
#include "BLEAdvertising.h"
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <BLE2901.h>
#include "esp_gap_ble_api.h" // <- Needed for esp_ble_gap_update_conn_params

uint32_t aPin = 36;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;
extern LedBlinker led;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *pServer) {
    deviceConnected = true;
    Serial.println("Client connected");

    esp_ble_conn_update_params_t conn_params = {0};
    //memcpy(conn_params.bda, pServer->getPeerAddress().getNative()->bda, sizeof(conn_params.bda));
    
    conn_params.min_int = 6;    // 6 * 1.25ms = 7.5ms
    conn_params.max_int = 12;   // 12 * 1.25ms = 15ms
    conn_params.latency = 0;
    conn_params.timeout = 200;  // 200 * 10ms = 2s supervision timeout

    esp_ble_gap_update_conn_params(&conn_params);
    led.set(1000,5);
  };

  void onDisconnect(BLEServer *pServer) {
    Serial.println("Client disconnected");
    deviceConnected = false;

    delay(500);  // Optional: let BLE stack settle before restart
    pServer->getAdvertising()->start();
    led.set(100,50);
  }
};

void BLE_setup() {
  // comms.startBLE():
}

// File: m370_communication.ino

class m370_communication {
  public:
    m370_communication();
    void setCharacteristic(BLECharacteristic *characteristic);
    void startBLE();
    void stopBLE();

    // Incoming (reading from BLE buffer)
    uint16_t getInput(uint8_t inBuf[], uint8_t *inInd);

    // Outgoing (building and sending packets)
    void outu8(uint8_t val);
    void out8(int8_t val);
    void outu16(uint16_t val);
    void out16(int16_t val);
    void outu32(uint32_t val);
    void out32(int32_t val);
    void outString(String val);
    uint16_t send(); // finalize and send outgoing packet
    void end(); // finalize and send outgoing packet

    // Buffer management
    void receiveByte(uint8_t b); // call this when you get incoming BLE bytes

    bool available() { return _available > 0; }

  private:
    void slipOut(uint8_t val);
    void pack(uint8_t val);

    static const uint8_t END_BYTE = 255;
    static const uint8_t ESC_BYTE = 254;
    static const uint8_t bufSize = 128; // or whatever you want

    // BLE references
    BLEServer* bleServer = nullptr;
    BLEService* bleService = nullptr;
    BLECharacteristic* bleCharacteristic = nullptr;
    BLEAdvertising* bleAdvertising = nullptr;
    BLE2901* descriptor_2901 = nullptr;

    // SLIP buffers
    uint8_t rawInBuffer[bufSize];
    uint8_t outBuffer[bufSize];
    uint16_t inWriteIndex = 0;
    uint16_t inReadIndex = 0;
    uint16_t outIndex = 0;

    volatile uint16_t _available = 0;

    bool enable = true;
    bool asciiDebug = false;
}; //end header

//IMPLEMENTATION

void m370_communication::startBLE() {
  // Fully reset BLE stack if needed
  led.set(200,50);
  BLEDevice::deinit();
  delay(100);

  // Format BLE name
  uint64_t mac = ESP.getEfuseMac(); // Get raw MAC address
  uint8_t mac4 = (mac >> 8) & 0xFF;
  uint8_t mac5 = mac & 0xFF;

  char bleName[16];
  snprintf(bleName, sizeof(bleName), "%s-%02X%02X", DEVICE_NAME, mac4, mac5);

  BLEDevice::init(bleName);

  Serial.print("BLE name: ");
  Serial.println(bleName);

  // Create BLE server and store reference
  bleServer = BLEDevice::createServer();
  bleServer->setCallbacks(new MyServerCallbacks());  // Define this elsewhere

  // Create service and store reference
  bleService = bleServer->createService(SERVICE_UUID);

  // Create characteristic and store reference
  bleCharacteristic = bleService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_WRITE |
    BLECharacteristic::PROPERTY_NOTIFY |
    BLECharacteristic::PROPERTY_INDICATE
  );

  // Add CCCD descriptor (0x2902)
  bleCharacteristic->addDescriptor(new BLE2902());

  if (bleCharacteristic) {
  Serial.println("Characteristic created successfully.");
} else {
  Serial.println("Failed to create characteristic!");
}

  // Add user description descriptor (0x2901)
  descriptor_2901 = new BLE2901();
  descriptor_2901->setDescription("My own description for this characteristic.");
  descriptor_2901->setAccessPermissions(ESP_GATT_PERM_READ);
  bleCharacteristic->addDescriptor(descriptor_2901);

  // Start the service
  bleService->start();

  // Get advertising instance and configure it
  bleAdvertising = BLEDevice::getAdvertising();
  bleAdvertising->addServiceUUID(SERVICE_UUID);
  bleAdvertising->setScanResponse(false);
  bleAdvertising->setMinPreferred(0x00);  // disables preferred connection param
  bleAdvertising->start();

  Serial.println("Waiting for a client connection to notify...");
}

void m370_communication::stopBLE() {
  if (bleAdvertising) {
    bleAdvertising->stop();
    Serial.println("BLE advertising stopped.");
  }

  BLEDevice::deinit();  // fully shuts down the BLE stack

  // clear stored pointers
  bleAdvertising = nullptr;
  bleServer = nullptr;
  bleService = nullptr;
  bleCharacteristic = nullptr;
  descriptor_2901 = nullptr;
}
  

  m370_communication::m370_communication() {}

  void m370_communication::setCharacteristic(BLECharacteristic *characteristic) {
    bleCharacteristic = characteristic;
  }

  // receiveByte: add a byte to the incoming buffer
  void m370_communication::receiveByte(uint8_t b) {
    rawInBuffer[inWriteIndex] = b;
    inWriteIndex = (inWriteIndex + 1) % bufSize;
  }

  // getInput: decode SLIP from rawInBuffer into inBuf
  uint16_t m370_communication::getInput(uint8_t inBuf[], uint8_t *inInd) {
    byte val;
    int inBufSize = *inInd;
    *inInd = 0;

    while (((inWriteIndex + bufSize - inReadIndex) % bufSize) > 0) {
      val = rawInBuffer[inReadIndex];
      inReadIndex = (inReadIndex < bufSize - 1) ? (inReadIndex + 1) : 0;

      if (val == ESC_BYTE) {
        inBuf[*inInd] = val;
        inReadIndex = (inReadIndex < bufSize - 1) ? (inReadIndex + 1) : 0;
        (*inInd)++;
      } else if (val == END_BYTE) {
        _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
        return _available;
      } else {
        inBuf[*inInd] = val;
        (*inInd)++;
      }
    }

    _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
    return _available;
  }

  // ========== Output Methods ==========

  void m370_communication::outu8(uint8_t val) { slipOut(val); }
  void m370_communication::out8(int8_t val) { slipOut((int)val + 128); }
  void m370_communication::outu16(uint16_t val) { slipOut(val >> 8); slipOut(val); }
  void m370_communication::out16(int16_t val) { uint16_t val2 = (int32_t)val + (1 << 15); slipOut(val2 >> 8); slipOut(val2); }
  void m370_communication::outu32(uint32_t val) { slipOut(val >> 24); slipOut(val >> 16); slipOut(val >> 8); slipOut(val); }
  void m370_communication::out32(int32_t val) { uint32_t val2 = (val < 0) ? ((1 << 15) - abs(val)) : (abs(val) + (1 << 31)); slipOut(val2 >> 24); slipOut(val2 >> 16); slipOut(val2 >> 8); slipOut(val2); }

  void m370_communication::outString(String val) {
    byte toSend[255];
    val.getBytes(toSend, 255);
    for (int i = 0; i < val.length(); i++) {
      slipOut(toSend[i]);
    }
  }

  void m370_communication::end() {
    pack(END_BYTE); // SLIP end
  }

  uint16_t m370_communication::send() {
    if (outIndex < 1) return 0;
    int sentBytes = -1;
    
    if (bleCharacteristic != nullptr) {
      bleCharacteristic->setValue(outBuffer, outIndex);
      bleCharacteristic->notify();
    //   for (int i = 0; i < outIndex; i++) {
    //     Serial.print(outBuffer[i], DEC);
    //     Serial.print(' ');
    //   }
    //   Serial.println();
    // Serial.print("BLE Notify: ");
    // Serial.println(outIndex);
    sentBytes = outIndex;
    }
    outIndex = 0;
    //slipOut(DEVICE_NUM);
    return sentBytes;
  }

  // ========== SLIP Encoding ==========

  void m370_communication::slipOut(uint8_t val) {
    if (val == END_BYTE || val == ESC_BYTE) {
      pack(ESC_BYTE);
      pack(val);
    } else {
      pack(val);
    }
  }

  void m370_communication::pack(uint8_t val) {
    if (outIndex < bufSize) {
      outBuffer[outIndex++] = val;
    }
  }