import os
import random
import sys
import time

import serial
from serial.tools import list_ports

serials = list(list_ports.comports())
attrs = ['device', 'name', 'description', 'hwid', 'vid', 'pid',
         'serial_number', 'location', 'manufacturer', 'product', 'interface']
for s in serials:
    [print(attr + ": " + str(getattr(s, attr))) for attr in attrs]
    print("\n")

exit()
ser = serial.Serial('COM18')  # open serial port
print(ser.name)         # check which port was really used
sys.stdout.flush()
try:
    while True:
        """inp = input('Text? ')
        inp += os.linesep"""
        inp = str(random.random()) + "\r"
        ser.write(str.encode(inp))     # write a string
        print(".")
        sys.stdout.flush()
        time.sleep(0.8)
except Exception as e:
    exit(e)
finally:
    ser.close()             # close port
