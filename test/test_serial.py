from serial.tools import list_ports
import serial
import os
import time
import sys
import random
#serials = list(list_ports.comports())
#[print(s) for s in serials]
ser = serial.Serial('COM20')  # open serial port
print(ser.name)         # check which port was really used
try:
    while True:
        """inp = input('Text? ')
        inp += os.linesep"""
        inp = str(random.random()) + "\r"
        ser.write(str.encode(inp))     # write a string
        print(".")
        sys.stdout.flush()
        time.sleep(0.8)
finally:
    ser.close()             # close port
