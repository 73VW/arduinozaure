"""Logging process."""
import re
import sys
import time
from multiprocessing import Event, Process

from serial import Serial

from .tools import get_arduino, load_config_from_arduino


class SerialReader(Process):
    """Process class."""

    def __init__(self, serial_port, parent):
        """Init process."""
        Process.__init__(self)
        self.exit = Event()
        self.serial_port = serial_port
        self.arduino = get_arduino(serial_port)
        self.get_port_list()
        self.value = dict()
        for port in self.ports:
            self.value[port] = 'Connection à la carte'
        self.ser = None
        self.parent = parent
        self.parent.set_datas(self.serial_port, self.value)
        print("Reader for " + serial_port + " inited")
        sys.stdout.flush()

    def get_port_list(self):
        """Get port list from config."""
        arduino = self.arduino
        (device_name, ports) = load_config_from_arduino(arduino)
        self.ports = {p: ports[p]
                      for p in ports if ports[p]['enabled'] is not ''}

    def get_datas(self):
        """Return datas."""
        return self.value

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            # Can't put it in init otherwise makes an error...
            self.ser = Serial(self.serial_port, timeout=None)
            try:
                self.read_serial()
            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
            finally:
                try:
                    self.ser.close()
                except AttributeError:
                    pass
        # print("You exited!")

    def shutdown(self):
        """Shut down process."""
        self.exit.set()

    def read_serial(self):
        """Read serial port."""
        pattern = re.compile(r'[\t\r\n]+')
        msg1 = 'My name is Arduinozaure. Send [ok] to start. Number of analogic pins: 6'
        msg2 = 'You can now ask a sensor value. Send me its pin number.'

        self.ser.read(self.ser.inWaiting())
        datas = re.sub(pattern, '', self.ser.readline().decode())
        while datas != msg1:
            time.sleep(0.4)
            datas = re.sub(pattern, '', self.ser.readline().decode())
        while datas != msg2:
            self.ser.read(self.ser.inWaiting())
            self.ser.write("ok".encode())
            time.sleep(0.4)
            datas = re.sub(pattern, '', self.ser.readline().decode())

        try:
            while(True):
                for port in self.ports:
                    self.ser.write(str.encode(str(port)))
                    data = re.sub(pattern, '',  self.ser.readline().decode())
                    self.value[port] = data
                self.parent.set_datas(self.serial_port, self.value)
        except (KeyboardInterrupt) as e:
            exit()
