import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)
rawString = arduino.readline()
print(rawString)
arduino.close()
