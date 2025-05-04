#nobby sensor input
#four pots and four buttons

def processInput(*args):
	raw_packet = args[0]  # extract bytes from the tuple
	name, sep, payload = raw_packet.partition(b':')
	val= list(payload)
	address = val.pop(0)
	device_name = name.decode()

	if sep != b':':
	    print("Malformed packet")
	# else:
	#     print("Device:", name.decode())
	#     print("Payload:", list(payload))

	# if sep != b':':
	#     print("Malformed packet (missing ':')!")
	# else:
	#     device_name = name.decode('utf-8')
	#     print(f"From {device_name}: {list(payload)}")
	# 	device_name = args[0][0]
	# 	address = args[0][1]
	# 	val = bto_ui16(args[0][2], args[0][3])

	#return("/sw0", 0)

	# I like to write this out longform in case I need
	#to change the order of sensors in a group
	#print(address, val)
	if address < 10:
		val = bto_ui16(val[0], val[1])
		if address == 0: return(device_name,"/analog0", val)
		elif address == 1: return(device_name,"/analog1", val)
		elif address == 2: return(device_name,"/analog2", val)
		elif address == 3: return(device_name,"/analog3", val)
		elif address == 4: return(device_name,"/analog4", val)
		elif address == 5: return(device_name,"/analog5", val)
	
	elif 10 <= address <= 18:
		#buttons
		#print("button", address)
		if address == 10: return(device_name,"/sw0", val)
		if address == 11: return(device_name,"/sw1", val)
		if address == 12: return(device_name,"/sw2", val)
		if address == 13: return(device_name,"/sw3", val)
		if address == 14: return(device_name,"/sw4", val)
		if address == 15: return(device_name,"/sw5", val)
		if address == 16: return(device_name,"/sw6", val)
		if address == 17: return(device_name,"/sw7", val)

	elif address == 30:
		#encoder
		return(device_name,"/enc0", -(val-(1<<15)))

	elif address == 31:
		return(device_name,"/encSw0", 1-val)

	elif 50 <= address <= 70:
		#capsense
		val = bto_i16(args[0][1], args[0][2]) #note using signed integer here
		if address == 50: return(device_name,"/cap0", val)
		elif address == 51: return(device_name,"/cap1", val)
		elif address == 52: return(device_name,"/cap2", val)
		elif address == 53: return(device_name,"/cap3", val)
		elif address == 54: return(device_name,"/cap4", val)
		elif address == 55: return(device_name,"/cap5", val)
		elif address == 56: return(device_name,"/cap6", val)
		elif address == 57: return(device_name,"/cap7", val)
		elif address == 58: return(device_name,"/cap8", val)
		elif address == 59: return(device_name,"/cap9", val)
		elif address == 60: return(device_name,"/cap10", val)
		elif address == 61: return(device_name,"/cap11", val)

	#accelerometer
	elif address == 71: # and len(args[0][1]) == 6: 
		try:
			aX = bto_i16(args[0][1], args[0][2]) / (1<<15)
			aY = bto_i16(args[0][3], args[0][4]) / (1<<15)
			aZ = bto_i16(args[0][5], args[0][6]) / (1<<15)
			return(device_name,"/acc0", [aX,aY,aZ])
		except Exception as e: 
			print(e)

	#gyroscope
	elif address == 72: # and len(args[0][1]) == 6: 
		try:
			gX = bto_i16(args[0][1], args[0][2])/ (1<<15)
			gY = bto_i16(args[0][3], args[0][4])/ (1<<15)
			gZ = bto_i16(args[0][5], args[0][6])/ (1<<15)
			return(device_name,"/gyro0", [gX,gY,gZ])
		except Exception as e: 
			print(e)

	print("no sensor assigned to this number", args[0][0])
	return(device_name,"/none0", 0)



def bto_ui16(high,low):
	#convert two bytes to a single unsigned 16-bit int
	return (high << 8) + low 

def bto_i16(high,low):
	#convert two bytes to a single signed 16-bit int
	val =  (high << 8) + low 
	val -= (1<<15)
	return val