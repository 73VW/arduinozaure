import io
import sys
import time

import serial

ser = serial.Serial('COM20', timeout=None)
ser.close()
exit()
print(ser.name)         # check which port was really used
terminator = b'\x03'
my_str = ""
sys.stdout.flush()
try:
    print("got: " + ser.read(ser.inWaiting()).decode())
    time.sleep(0.3)
    print("got: " + ser.readline().decode())
    print("sent: ok")
    ser.write(str.encode("ok"))
    print("got: " + ser.readline().decode())
    print("sent: 5")
    ser.write(str.encode("5"))
    print("got: " + ser.readline().decode())
    sys.stdout.flush()
finally:
    ser.close()
