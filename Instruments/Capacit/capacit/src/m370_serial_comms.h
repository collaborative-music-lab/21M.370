#ifndef M370_SERIAL_COMMS_h
#define M370_SERIAL_COMMS_h
#include "Arduino.h"
#include "BluetoothSerial.h"  // Include Bluetooth Serial library


/************************
**Communication class
************************/


class m370_serial_comms{
	public:
	m370_serial_comms();
	m370_serial_comms(uint16_t size); //buffer sizes in bytes, def:64

	uint8_t begin( ); //returns success or failure
	uint8_t connect(); //returns 1=serial, 2=wifi, 3=bluetooth

	//uint16_t checkInput();
	uint16_t available();
	uint16_t getInput(uint8_t *inBuf, uint8_t *inInd);

	void outu8(uint8_t val);
	void out8(int8_t val);
	void outu16(uint16_t val);
	void out16(int16_t val);
	void outu32(uint32_t val);
	void out32(int32_t val);
	void outString(String val);

	uint16_t send();

	byte enable = 1;
	byte asciiDebug = 0;
	int baudRate = 460800;

	  //below all auto configured based  on comMode
	byte SERIAL_ENABLE = 0; //enables communication over USB
	byte ACTIVE_MODE = 0; //1=serial,2=wifi, 3=blutooth
	byte BLUETOOTH_ENABLE = 0;

	byte handshakeAck = 0;
	byte serverFound=0;
	  
	private:
	void Init(uint16_t size);
	void pack(byte val);
	void slipOut(byte val);

	uint16_t bufSize;
	
	//slip decoded buffer
	byte inBuffer[64];
	uint8_t inIndex = 0;
	//raw input
	byte *rawInBuffer;
	uint8_t inWriteIndex = 0;
	uint8_t inReadIndex = 0;

	byte *outBuffer;
	uint8_t outIndex = 0;

	uint16_t _available = 0;

	uint8_t serial_setup();
	uint8_t bluetooth_setup();

  
  	// define end bytes and escape bytes needed for slip encoding
	const byte END_BYTE = 255;
	const byte ESC_BYTE = 254;
};

#endif
