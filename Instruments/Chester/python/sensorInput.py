#nobby sensor input
#four pots and four buttons

def processInput(*args):
	address = args[0][0]
	val = bto_ui16(args[0][1], args[0][2])

	# I like to write this out longform in case I need
	#to change the order of sensors in a group
	#print(address, val)
	if address == 0: return("/pot0", val)
	elif address == 1: return("/pot1", val)
	elif address == 2: return("/pot2", val)
	elif address == 3: return("/pot3", val)
	elif address == 4: return("/pot4", val)
	elif address == 5: return("/pot5", val)
	
	elif 10 <= address <= 18:
		#buttons
		#print("button", address)
		if address == 10: return("/sw0", val)
		if address == 11: return("/sw1", val)
		if address == 12: return("/sw2", val)
		if address == 13: return("/sw3", val)
		if address == 14: return("/sw4", val)
		if address == 15: return("/sw5", val)
		if address == 16: return("/sw6", val)
		if address == 17: return("/sw7", val)

	elif 50 <= address <= 70:
		#capsense
		val = bto_i16(args[0][1], args[0][2]) #note using signed integer here
		if address == 50: return("/cap0", val)
		elif address == 51: return("/cap1", val)
		elif address == 52: return("/cap2", val)
		elif address == 53: return("/cap3", val)
		elif address == 54: return("/cap4", val)
		elif address == 55: return("/cap5", val)
		elif address == 56: return("/cap6", val)
		elif address == 57: return("/cap7", val)
		elif address == 58: return("/cap8", val)
		elif address == 59: return("/cap9", val)
		elif address == 60: return("/cap10", val)
		elif address == 61: return("/cap11", val)

	elif 71<= address <= 72:
		#accelerometer
		if address == 71: # and len(args[0][1]) == 6: 
			try:
				aX = bto_i16(args[0][1], args[0][2]) / (1<<15)
				aY = bto_i16(args[0][3], args[0][4]) / (1<<15)
				aZ = bto_i16(args[0][5], args[0][6]) / (1<<15)
				return("/acc0", [aX,aY,aZ])
			except Exception as e: 
				print(e)
		#gyroscope
		elif address == 72: # and len(args[0][1]) == 6: 
			try:
				gX = bto_i16(args[0][1], args[0][2])/ (1<<15)
				gY = bto_i16(args[0][3], args[0][4])/ (1<<15)
				gZ = bto_i16(args[0][5], args[0][6])/ (1<<15)
				return("/gyro0", [gX,gY,gZ])
			except Exception as e: 
				print(e)

	print("no sensor assigned to this number", args[0][0])
	return("/none0", 0)



def bto_ui16(high,low):
	#convert two bytes to a single unsigned 16-bit int
	return (high << 8) + low 

def bto_i16(high,low):
	#convert two bytes to a single signed 16-bit int
	val =  (high << 8) + low 
	val -= (1<<15)
	return val