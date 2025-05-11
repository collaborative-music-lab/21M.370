 /* Simple test for analog and digital inputs, and digital outputs
 * 
 */
#include "m370_lbr.h"
#include <Wire.h> 

 byte SERIAL_DEBUG = 0;
 byte IMU_DEBUG = 0;


////Firmware metadata
String FIRMWARE[] = {
  /*NAME*/ "chester",
  /*VERSION*/ "0.2",
  /*AUTHOR*/ "Ian Hattwick",
  /*DATE*/ "Apr 15, 2025",
  /*NOTES*/ "Serial Only"
};


//set comMode to SERIAL_ONLY here:
const comModes comMode = SERIAL_ONLY;
m370_communication comms(comMode);


/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 0;

m370_analog ana[6] = {
  m370_analog(p0,20), //pin, sampling rate (Hz) F = 1/T, T = 1/F
  m370_analog(p1,20),  //pin, sampling rate (Hz)
  m370_analog(p2,20), //pin, sampling rate (Hz)
  m370_analog(p3,20),  //pin, sampling rate (Hz)
  m370_analog(p4,20), //pin, sampling rate (Hz)
  m370_analog(p5,20)  //pin, sampling rate (Hz)
};

/*********************************************
DIGITAL INPUT SETUP
*********************************************/
const byte NUM_DIGITAL = 4;

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
 
  comms.baudRate = 115200;
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
  //for(byte i=0;i<NUM_ANALOG;i++) ana[i].begin();
  //enc.begin([]{enc.readEncoder_ISR();});
  //imuSetup();

  Serial.println("Setup complete");
}
const int microphonePin = 32;
float oldval = 0;
float alpha = 0.95;
uint32_t timer = 0;
uint32_t rtimer = 0;
int photocellPin = 39;
int photocellReading;
void loop() {
  float delta = analogRead(microphonePin);
  photocellReading = analogRead(photocellPin);

  static uint32_t timer = 0;
  if(millis() - timer > 2){
    timer = millis();
    oldval = delta*(1-alpha)+oldval*alpha;
  }

  if((millis()-rtimer)>= 100){
    rtimer = millis();
    if(SERIAL_DEBUG){
      Serial.print("Average:");
      Serial.println(oldval);
      Serial.println("Sent");
      Serial.println(photocellReading);
    }
    else{
      comms.outu8(0);
      comms.outu16(photocellReading);
      comms.send();
      comms.outu8(1);
      comms.outu16(oldval);
      comms.send();
    
    }
  }
  readSw();
  //readAnalog();
  //readEncoder();
  //imuLoop();
}

void readSw(){
  static int count[4];
  
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
  for(int i=0;i<NUM_ANALOG;i++){
    ana[i].loop();
    if(ana[i].available() ){
      int outVal = ana[i].getVal();
      if( SERIAL_DEBUG ) {
        PrintDebug("analog",i,outVal);
      }
      else {
        comms.outu8(i);
        comms.outu16(outVal);
        comms.send();
      }
    }
  }
}


void PrintDebug(String name, int num, int val){
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
