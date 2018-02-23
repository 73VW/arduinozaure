import serial
import io
import sys
ser = serial.Serial('COM18', timeout=None)
print(ser.name)         # check which port was really used
terminator = b'\x03'
my_str = ""
sys.stdout.flush()
try:
    while ser.is_open:
        data = ser.read(ser.inWaiting())
        if data is terminator:
            print("terminator")
            break
        data_str = data.decode()
        if data_str is "\r":
            data_str = "\n\r"
        print(data_str, end='')
        my_str += data_str
        sys.stdout.flush()
finally:
    ser.close()
