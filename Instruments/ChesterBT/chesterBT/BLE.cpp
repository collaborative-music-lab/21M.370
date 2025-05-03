// #include "m370_communication.h"

// const byte COMM_DEBUG = 0;
// BluetoothSerial BTSerial;

// //Are we currently connected?
// boolean connected2 = false;
// boolean serverFound = false;


// /*********************************************
// CONSTRUCTOR
// *********************************************/

// m370_communication::m370_communication(comModes _mode, uint16_t size){
//   Init(size);
//   mode = _mode;
// }

// m370_communication::m370_communication(comModes _mode){
//   Init(64);
//   mode = _mode;
// }

// m370_communication::m370_communication(){
//   Init(64);
// }


// void m370_communication::Init(uint16_t size){
//   bufSize=size;
//   rawInBuffer = new uint8_t(bufSize);
//   outBuffer = new uint8_t(bufSize);
// }

// uint8_t m370_communication::begin(){
//     enable = 1;
//     inWriteIndex = 0;
//     inReadIndex = 0;
    
//     Init(bufSize);
//     serial_setup();  // Only setup Serial
//     Serial.println("comms begin");
//     bluetooth_setup();  // Set up Bluetooth Serial
//     Serial.println("begin done");
//     return 1;
// }

// /*********************************************
// SETUP FUNCTIONS
// *********************************************/

// uint8_t m370_communication::serial_setup(){
//   Serial.begin(baudRate);
//   delay(200);
//   if( COMM_DEBUG ) Serial.println("Serial initialized");
//   //m370_wifiConnectionState=1;
//   SERIAL_ENABLE = 1;
//   return 1;
// }

// // Initialize Bluetooth Serial
// uint8_t m370_communication::bluetooth_setup() {
//   const unsigned long pairingTimeout = 30000; // 30 seconds
//   const char* deviceName = "ChesterBT";
//   char pinCode[] = "1234";// Optional PIN for pairing security

//   byte pairingButtonPin = 13;
//   pinMode(pairingButtonPin, INPUT_PULLUP); // GPIO0 with pull-up resistor
//   byte buttonState = digitalRead(pairingButtonPin);
//   if (buttonState == LOW) {
//     // Button held down → Pairing Mode
//     Serial.println("Booted into PAIRING MODE");
//     pairingMode = 1;

//     pairingStartTime = millis();

//     BTSerial.begin(deviceName, true);  // true = enable secure pairing
//     //BTSerial.setPin("1234"); //doesn't work

//     Serial.println("Device paired successfully!");
//     Serial.println(pairingMode);
//   } else {
//     // Normal Mode
//     BTSerial.begin(deviceName); // normal mode: no forced pairing
//     Serial.println("Booted into NORMAL MODE, ready for connection.");
//     Serial.println(pairingMode);
//   }
//   Serial.println("end");
// }

// uint8_t m370_communication::bluetooth_loop() {
//   if (pairingMode) {
//     unsigned long elapsed = millis() - pairingStartTime;

//     if (BTSerial.hasClient()) {
//       Serial.println("Client trying to connect...");
//       if (BTSerial.connected()) {
//         Serial.println("Client connected successfully!");

//         // ✅ Exit pairing mode cleanly
//         pairingMode = false;
//         // (Optional: ESP.restart(); if you want a clean reboot)
//       }
//     } else if (elapsed > 30000) {
//       Serial.println("Pairing timeout. Restarting into normal mode...");
//       delay(100);
//       ESP.restart();
//     } else {
//       // Still waiting: print every second
//       static unsigned long lastPrint = 0;
//       if (millis() - lastPrint > 1000) {
//         lastPrint = millis();
//         Serial.print("Waiting for pairing... ");
//         Serial.print(elapsed / 1000);
//         Serial.println("s elapsed");
//       }
//     }
//     return 1;
//   } else {
//     // Normal operation
//     // if (BTSerial.available()) {
//     //   Serial.write(BTSerial.read());
//     // }
//     return 0;
//   }
//   return 0;
// }
// /*********************************************
// INPUT
// *********************************************/

// //Stores raw slip encoded data in input buffer, and returns
// //number of available bytes
// uint16_t m370_communication::available(){
//   if(1){
//     while(Serial.available()) {
//       ACTIVE_MODE = 1;
//       inWriteIndex<bufSize-1 ? inWriteIndex++ : inWriteIndex=0 ;
//       rawInBuffer[inWriteIndex] = Serial.read();
//       if(COMM_DEBUG){
//         Serial.print('w');
//         Serial.write( inWriteIndex );
//       }
//     }
//     while (BTSerial.available()) {
//         inWriteIndex = (inWriteIndex + 1) % bufSize;
//         rawInBuffer[inWriteIndex] = BTSerial.read();
//     }
//   }
  
  
//   _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;

//   return _available;
// }

// // uint16_t m370_communication::slipDecode(byte val){

// // }

// //uint16_t m370_communication::available(){ return _available;}

// uint16_t m370_communication::getInput(uint8_t inBuf[], uint8_t *inInd){
//   byte val;
//   int inBufSize = *inInd;
//   *inInd=0;

//   while( ((inWriteIndex+bufSize-inReadIndex)%bufSize) > 0) {
//     val = rawInBuffer[inReadIndex];
//     inReadIndex<bufSize-1 ? inReadIndex++ : inReadIndex=0 ;
//     //slip decode
//     if(val==ESC_BYTE){
//       if(1){ //*inInd < inBufSize) {
//         inBuf[*inInd]  = val;
//         inReadIndex<bufSize-1 ? inReadIndex++ : inReadIndex=0 ;
//         *inInd+=1;
//       }
//     } else if(val==END_BYTE){
//       _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
//       if(COMM_DEBUG){
//         Serial.print('a');
//         Serial.print(_available);
//         Serial.print('g');
//         Serial.print(*inInd);
//         for(int i=0;i<*inInd;i++)Serial.print(inBuf[i]);
//         Serial.println('g');
//       }
//       return _available;
//     } else {
//       if(1){ //*inInd < inBufSize) {
//         inBuf[*inInd]  = val;
//         *inInd+=1;
//       }
//     }//slip

//   }//while
//   if(COMM_DEBUG){
//     Serial.print('h');
//         for(int i=0;i<*inInd;i++)Serial.print(inBuf[i]);
//           Serial.print('h');
//     }
//   _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
//   return _available;
// }


// /*********************************************
// OUTPUT
// *********************************************/

// void m370_communication::outu8(uint8_t val){
//   slipOut(val);
// }

// void m370_communication::out8(int8_t val){
//   uint8_t val2 = (int)val+128;
//   slipOut(val2);
// }

// void m370_communication::outu16(uint16_t val){
//   slipOut(val>>8);
//   slipOut( val );
// }

// void m370_communication::out16(int16_t val){
//   uint16_t val2 = (int32_t)val + (1<<15);
//   slipOut(val2>>8);
//   slipOut(val2);
// }

// void m370_communication::outu32(uint32_t val){
//   slipOut(val>>24);
//   slipOut(val>>16);
//   slipOut(val>>8);
//   slipOut(val);
// }
// void m370_communication::out32(int32_t val){
//   uint32_t val2 = abs(val);
//   val < 0 ? val2 = (1<<15) - val2  : val2 += (1<<31);
//   slipOut(val2>>24);
//   slipOut(val2>>16);
//   slipOut(val2>>8);
//   slipOut(val2);
// }

// void m370_communication::outString(String val){
//   byte toSend[255];
//   val.getBytes(toSend,255);
//   for(int i=0;i<val.length();i++) slipOut(toSend[i]);
// }

// uint16_t m370_communication::send(){
//   if(outIndex<1) return 0;
//   pack(255);
//   //addEndByte();
//   // Serial.print("Sent: ")
//   // Serial.print(outIndex);

//   if(enable){
//     if(asciiDebug) {
//       for(byte i=0;i<outIndex;i++){
//         Serial.print (outBuffer[i]);
//         Serial.print(" ");
//         }
//       }
//     //serial
//     else if(ACTIVE_MODE==1){ //else if(SERIAL_ENABLE){
//       for(byte i=0;i<outIndex;i++){
//         //Serial.write(outBuffer[i]);
//         BTSerial.write(outBuffer[i]);
//       }
//     }
//     uint16_t  returnValue =   outIndex;
//     outIndex = 0;
//     return  returnValue;
//   }
// }//send

// void m370_communication::slipOut(byte val){
//   if(val == END_BYTE || val == ESC_BYTE){
//     pack(ESC_BYTE);
//     pack(val);
//   } else pack(val);
// }

// void m370_communication::pack(byte val){
//   outBuffer[outIndex++] = val;
// }