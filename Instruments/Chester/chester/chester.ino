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
ENCODERS SETUP 
*********************************************/
//encoders rely on the  ESP32Encoder library
//Esp32Encoder rotaryEncoder = Esp32Encoder(18,2,4);//A,B,Button
//optional divider argument
//arguments:
// - A and B: digital inputs from encoder
// - Switch; pin for encoder switch, or -1 for no switch
// - divider: many encoders put out multiple pulses per detent
//   The divider helps to make encoder increments match detents

Esp32Encoder enc(p10,p11,p13,1);//A,B,Switch, Divider

/*********************************************
ANALOG SETUP
*********************************************/
const byte NUM_ANALOG = 4;

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
  //enc.begin([]{enc.readEncoder_ISR();});
  imuSetup();

  Serial.println("Setup complete");
}

void loop() {
  readSw();
  readAnalog();
  //readEncoder();
  imuLoop();

  
  if (comms.available()){
    byte inBuffer[64];
    byte index=0;

    comms.getInput(inBuffer,  &index);
  }
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

void readEncoder(){
  byte curB = enc.button(); //get current button state
  //four button states:
  // - 0 for button is being held down
  // - 1 for button transition from not pushed to pushed
  // - 2 for button is not being held down
  // - 3 for button transition from pushed to not pushed

  int val = enc.delta(); //get encoder  count
  if(val!= 0){
    if(SERIAL_DEBUG){
      Serial.print("count: ");
      Serial.println(val);
    }
    else{
      comms.outu8(30);
      comms.out16( val );
      comms.send();
    }
  }

  switch(curB){
    case 0: //DOWN
    break;

    case 1: //PUSHED
    if(SERIAL_DEBUG) Serial.println("PUSHED");
    else{
      comms.outu8(31);
      comms.outu16(1);
      comms.send();
    }
    break;

    case 2: //UP
   
    break;

    case 3: //RELEASED
    if(SERIAL_DEBUG) Serial.println("RELEASED");
    else{
      comms.outu8(31);
      comms.outu16(0);
      comms.send();
    }
    break;
  }//switch
}

void PrintDebug(String name, int num, int val){
  Serial.print(name);
  Serial.print(" ");
  Serial.print(num);
  Serial.print(": ");
  Serial.println(val);
}
