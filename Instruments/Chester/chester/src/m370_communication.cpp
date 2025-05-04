#include "m370_communication.h"

const byte COMM_DEBUG = 0;

extern const char * ssid;
extern const char * password;
extern const char * port;


/*********************************************
CONSTRUCTOR
*********************************************/

m370_communication::m370_communication(comModes _mode, uint16_t size){
  Init(size);
  mode = _mode;
}

m370_communication::m370_communication(comModes _mode){
  Init(64);
  mode = _mode;
}

m370_communication::m370_communication(){
  Init(64);
}


void m370_communication::Init(uint16_t size){
  bufSize=size;
  rawInBuffer = new uint8_t(bufSize);
  outBuffer = new uint8_t(bufSize);
}

uint8_t m370_communication::begin( String firmwareNotes[5]){
  enable=1;
  inWriteIndex=0;
  inReadIndex=0;
  _firmwareNotes = firmwareNotes;

  Init(bufSize);
  uint8_t returnVal=0;
  Serial.begin(baudRate);

  // while(1) { 
  //   //Serial.begin(baudRate);
  //   delay(200);
  //   Serial.println("comm mode" + String(mode));
  // }

  if( mode==SERIAL_ONLY || mode==APandSERIAL || mode==STAandSERIAL) returnVal =  serial_setup();
  if( mode==SERIAL_ONLY) {
    ACTIVE_MODE = 1;
  }
  return returnVal>0;
}

/*
connect() listens for incoming messages on all specific interfaces
and returns a value based on the first interface it hears from:
1 = serial
2 = wifi
2 = bluetooth (not  implemented)

Typically connect will be called from a while  loop in a setup functtion
This allows the ucontroller to perform specific tasks to indicate connect status
*/
uint8_t m370_communication::connect(){
  //handshaking
  byte numAvailable = available();
  Serial.println("connect ");


  
  return 1;
}


/*********************************************
SETUP FUNCTIONS
*********************************************/

uint8_t m370_communication::serial_setup(){
  //Serial.begin(baudRate);
  delay(200);
  if( COMM_DEBUG ) Serial.println("Serial initialized");
  //m370_wifiConnectionState=1;
  SERIAL_ENABLE = 1;
  return 1;
}

/*********************************************
INPUT
*********************************************/

//Stores raw slip encoded data in input buffer, and returns
//number of available bytes
uint16_t m370_communication::available(){
    while(Serial.available()) {
      ACTIVE_MODE = 1;
      inWriteIndex<bufSize-1 ? inWriteIndex++ : inWriteIndex=0 ;
      rawInBuffer[inWriteIndex] = Serial.read();
      if(COMM_DEBUG){
        Serial.print('w');
        Serial.write( inWriteIndex );
      }
    }
  
  _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;

  return _available;
}

uint16_t m370_communication::getInput(uint8_t inBuf[], uint8_t *inInd){
  byte val;
  int inBufSize = *inInd;
  *inInd=0;

  while( ((inWriteIndex+bufSize-inReadIndex)%bufSize) > 0) {
    val = rawInBuffer[inReadIndex];
    inReadIndex<bufSize-1 ? inReadIndex++ : inReadIndex=0 ;
    //slip decode
    if(val==ESC_BYTE){
      if(1){ //*inInd < inBufSize) {
        inBuf[*inInd]  = val;
        inReadIndex<bufSize-1 ? inReadIndex++ : inReadIndex=0 ;
        *inInd+=1;
      }
    } else if(val==END_BYTE){
      _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
      if(COMM_DEBUG){
        Serial.print('a');
        Serial.print(_available);
        Serial.print('g');
        Serial.print(*inInd);
        for(int i=0;i<*inInd;i++)Serial.print(inBuf[i]);
        Serial.println('g');
      }
      return _available;
    } else {
      if(1){ //*inInd < inBufSize) {
        inBuf[*inInd]  = val;
        *inInd+=1;
      }
    }//slip

  }//while
  if(COMM_DEBUG){
    Serial.print('h');
        for(int i=0;i<*inInd;i++)Serial.print(inBuf[i]);
          Serial.print('h');
    }
  _available = (inWriteIndex + bufSize - inReadIndex) % bufSize;
  return _available;
}


/*********************************************
OUTPUT
*********************************************/

void m370_communication::outu8(uint8_t val){
  slipOut(val);
}

void m370_communication::out8(int8_t val){
  uint8_t val2 = (int)val+128;
  slipOut(val2);
}

void m370_communication::outu16(uint16_t val){
  slipOut(val>>8);
  slipOut( val );
}

void m370_communication::out16(int16_t val){
  uint16_t val2 = (int32_t)val + (1<<15);
  slipOut(val2>>8);
  slipOut(val2);
}

void m370_communication::outu32(uint32_t val){
  slipOut(val>>24);
  slipOut(val>>16);
  slipOut(val>>8);
  slipOut(val);
}
void m370_communication::out32(int32_t val){
  uint32_t val2 = abs(val);
  val < 0 ? val2 = (1<<15) - val2  : val2 += (1<<31);
  slipOut(val2>>24);
  slipOut(val2>>16);
  slipOut(val2>>8);
  slipOut(val2);
}

void m370_communication::outString(String val){
  byte toSend[255];
  val.getBytes(toSend,255);
  for(int i=0;i<val.length();i++) slipOut(toSend[i]);
}

uint16_t m370_communication::send(){
  if(outIndex<1) return 0;
  pack(255);

  if(enable){
    if(asciiDebug) {
      for(byte i=0;i<outIndex;i++){
        Serial.print (outBuffer[i]);
        Serial.print(" ");
        }
      }
    //serial
    else{ //else if(SERIAL_ENABLE){
      for(byte i=0;i<outIndex;i++){
        Serial.write(outBuffer[i]);
      }
    }
    
    uint16_t  returnValue =   outIndex;
    outIndex = 0;
    return  returnValue;
  }
}//send

void m370_communication::slipOut(byte val){
  if(val == END_BYTE || val == ESC_BYTE){
    pack(ESC_BYTE);
    pack(val);
  } else pack(val);
}

void m370_communication::pack(byte val){
  outBuffer[outIndex++] = val;
}