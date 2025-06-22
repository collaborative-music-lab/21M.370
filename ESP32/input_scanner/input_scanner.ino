 /* Simple test for analog and digital inputs, and digital outputs
 * 
 */
#include "m370_lbr.h"
#include <Wire.h> 

 byte SERIAL_DEBUG = 1;
 byte IMU_DEBUG = 0;


////Firmware metadata
String FIRMWARE[] = {

};


//set comMode to SERIAL_ONLY here:
const comModes comMode = SERIAL_ONLY;
m370_communication comms(comMode);


/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 6;

m370_analog ana[6] = {
  m370_analog(p0,200), //pin, sampling rate (Hz) F = 1/T, T = 1/F
  m370_analog(p1,200),  //pin, sampling rate (Hz)
  m370_analog(p2,20), //pin, sampling rate (Hz)
  m370_analog(p3,20),  //pin, sampling rate (Hz)
  m370_analog(p4,20), //pin, sampling rate (Hz)
  m370_analog(p5,20)  //pin, sampling rate (Hz)
};

/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 8;

m370_digitalInput sw[8] = {
  m370_digitalInput(p6,500),//pin, rate(Hz)
  m370_digitalInput(p7,500),//pin, rate(Hz)
  m370_digitalInput(p8,500),//pin, rate(Hz)
  m370_digitalInput(p9,500),//pin, rate(Hz)
  m370_digitalInput(p10,500),//pin, rate(Hz)
  m370_digitalInput(p11,500),//pin, rate(Hz)
  m370_digitalInput(p12,500),//pin, rate(Hz)
  m370_digitalInput(p13,500)//pin, rate(Hz)
};


void setup() {
 
  comms.baudRate = 460800;
  comms.begin(FIRMWARE);
  
  byte commsBegin = 0;
  while(commsBegin  ==  0){
    if(SERIAL_DEBUG == 2) commsBegin = 1;
    Serial.println("comms");
    commsBegin = comms.connect()  ; //sends firmware metadata to begin function
    
    }

  delay(100);

  //initialize inputs
  for( int i=0;i<NUM_DIGITAL;i++) sw[i].begin();
  for(byte i=0;i<NUM_ANALOG;i++) ana[i].begin();

  Serial.println("Setup complete");
}

void loop() {
  readSw();
  readAnalog();

  delay(100);
}

void readSw(){
  static int count[8];
  
  for(int i=0;i<NUM_DIGITAL;i++){
    sw[i].loop();
    if( sw[i].available() ){
      int outVal = sw[i].getState();
      if(outVal==1) count[i]++;
      if( SERIAL_DEBUG ) {
        PrintDebug("sw",i,count[i]);
      }
      else {
        comms.outu8(i+10);
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}

void readAnalog(){
  byte enPrint = 0;
  static int val[] = {0,0,0,0,0,0};
  for(int i=0;i<NUM_ANALOG;i++){
    ana[i].loop();
    if(ana[i].available() ){
      int outVal = ana[i].getVal();
      int delta = abs(val[i] - outVal); 
     
      if( SERIAL_DEBUG) {
        // Serial.print(delta < 10 ? 0 : delta-10);
        //Serial.print("\t");
        // Serial.print(outVal);
        
        if(delta > 100){
          val[i] = outVal;
          enPrint = 1;
          Serial.print(i);
          Serial.print(',');
          Serial.print(espPin[i]);
          Serial.print(',');
          Serial.print(outVal);
          Serial.println();

        }
      }
      else {
        comms.outu8(i);
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
  //if(enPrint && SERIAL_DEBUG) Serial.println();
}

void PrintDebug(String name, int num, int val){
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
