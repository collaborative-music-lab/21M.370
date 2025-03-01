#include "m370_serial_comms.h"

// Debug flag
const byte COMM_DEBUG = 0;
//BluetoothSerial BTSerial;  // Create Bluetooth Serial object

/*********************************************
  CONSTRUCTORS
*********************************************/
m370_serial_comms::m370_serial_comms(uint16_t size) {
    Init(size);
}

m370_serial_comms::m370_serial_comms() {
    Init(64);
}

// Initialize buffers
void m370_serial_comms::Init(uint16_t size) {
    bufSize = size;
    rawInBuffer = new uint8_t(bufSize);
    outBuffer = new uint8_t(bufSize);
}

// Begin communication (Serial-Only)
uint8_t m370_serial_comms::begin() {
    enable = 1;
    inWriteIndex = 0;
    inReadIndex = 0;
    
    Init(bufSize);
    serial_setup();  // Only setup Serial

    bluetooth_setup();  // Set up Bluetooth Serial
    return 1;
}

/*********************************************
  CONNECT FUNCTION (Always Returns Serial Connection)
*********************************************/
uint8_t m370_serial_comms::connect() {
    byte numAvailable = available();

    if (numAvailable > 0) {
        getInput(inBuffer, &inIndex);
        for (int i = 0; i < inIndex; i++) {
            Serial.print(inBuffer[i]);
        }
        send();
    }
    return 1;  // Always return a valid connection since it's serial-only
}

/*********************************************
  SERIAL SETUP FUNCTION
*********************************************/
uint8_t m370_serial_comms::serial_setup() {
    Serial.begin(115200);
    delay(200);
    
    if (COMM_DEBUG) {
        Serial.println("Serial initialized");
    }

    return 1;
}

// Initialize Bluetooth Serial
uint8_t m370_serial_comms::bluetooth_setup() {
    //BTSerial.begin("ESP32_BT");  // Set Bluetooth name
    Serial.println("Bluetooth Serial Started: ESP32_BT");
    return 1;
}

/*********************************************
  INPUT FUNCTION
*********************************************/
uint16_t m370_serial_comms::available() {
    if (Serial.available()) {
        inWriteIndex = (inWriteIndex + 1) % bufSize;
        rawInBuffer[inWriteIndex] = Serial.read();
    }
    // if (BTSerial.available()) {
    //     inWriteIndex = (inWriteIndex + 1) % bufSize;
    //     rawInBuffer[inWriteIndex] = BTSerial.read();
    // }
    return (inWriteIndex + bufSize - inReadIndex) % bufSize;
}

uint16_t m370_serial_comms::getInput(uint8_t inBuf[], uint8_t *inInd) {
    byte val;
    int inBufSize = *inInd;
    *inInd = 0;

    while (((inWriteIndex + bufSize - inReadIndex) % bufSize) > 0) {
        val = rawInBuffer[inReadIndex];
        inReadIndex = (inReadIndex + 1) % bufSize;

        if (val == END_BYTE) {
            return (inWriteIndex + bufSize - inReadIndex) % bufSize;
        } else {
            inBuf[*inInd] = val;
            (*inInd)++;
        }
    }
    return (inWriteIndex + bufSize - inReadIndex) % bufSize;
}

/*********************************************
  OUTPUT FUNCTION
*********************************************/
void m370_serial_comms::outu8(uint8_t val){
  slipOut(val);
}

void m370_serial_comms::out8(int8_t val){
  uint8_t val2 = (int)val+128;
  slipOut(val2);
}

void m370_serial_comms::outu16(uint16_t val){
  slipOut(val>>8);
  slipOut( val );
}

void m370_serial_comms::out16(int16_t val){
  uint16_t val2 = (int32_t)val + (1<<15);
  slipOut(val2>>8);
  slipOut(val2);
}

void m370_serial_comms::outu32(uint32_t val){
  slipOut(val>>24);
  slipOut(val>>16);
  slipOut(val>>8);
  slipOut(val);
}
void m370_serial_comms::out32(int32_t val){
  uint32_t val2 = abs(val);
  val < 0 ? val2 = (1<<15) - val2  : val2 += (1<<31);
  slipOut(val2>>24);
  slipOut(val2>>16);
  slipOut(val2>>8);
  slipOut(val2);
}

void m370_serial_comms::outString(String val){
  byte toSend[255];
  val.getBytes(toSend,255);
  for(int i=0;i<val.length();i++) slipOut(toSend[i]);
}

// uint16_t m370_serial_comms::send() {
//     if (outIndex < 1) return 0;

//     for (byte i = 0; i < outIndex; i++) {
//         Serial.write(outBuffer[i]);
//         BTSerial.write(outBuffer[i]);
//     }

//     uint16_t returnValue = outIndex;
//     outIndex = 0;
//     return returnValue;
// }
uint16_t m370_serial_comms::send() {
    if (outIndex < 1) return 0;
    pack(255);

    if(0) {
        for (byte i = 0; i < outIndex; i++) {
         Serial.print(outBuffer[i]);
     }
     Serial.println();
    }
    else{
       // Send entire buffer at once for minimal overhead
        Serial.write(outBuffer, outIndex);
        //BTSerial.write(outBuffer, outIndex);
    }

    uint16_t returnValue = outIndex;
    outIndex = 0;  // Reset buffer index after sending

    return returnValue;
}

void m370_serial_comms::slipOut(byte val){
  if(val == END_BYTE || val == ESC_BYTE){
    pack(ESC_BYTE);
    pack(val);
  } else pack(val);
}

void m370_serial_comms::pack(byte val){
  outBuffer[outIndex++] = val;
}

