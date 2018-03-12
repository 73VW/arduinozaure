"""Logging process."""
import re
import sys
import time
from multiprocessing import Event
from multiprocessing import Manager
from multiprocessing import Process

from serial import Serial
from settings import DEVICE_CONFIG_FOLDER
from settings import path
from yaml import safe_load

from models.device import Device
from models.sensor import Sensor


class SerialReader(Process):
    """Process class."""

    def __init__(self, serial_port, parent):
        """Init process."""
        Process.__init__(self)
        self.exit = Event()
        self.serial_port = serial_port
        self.device = Device.get(Device.get_identifier_from_serial(serial_port))
        self.get_port_list()
        self.ser = None
        self.parent = parent
        self.parent.set_datas(self.serial_port, dict(self.value))
        print("Reader for " + serial_port + " inited")
        sys.stdout.flush()

    def get_port_list(self):
        """Get port list from config."""
        self.ports = Manager().dict()
        self.value = Manager().dict()
        self.sensors = dict()
        for p in self.device.ports['input']:
            if p.enabled:
                self.ports[p.number] = p
                self.value[p.number] = 'Connection à la carte'
                self.sensors[p.number] = Sensor.get(p._type)

    def get_datas(self):
        """Return datas."""
        return self.value

    def run(self):
        """Run process."""
        self.init_serial()
        while not self.exit.is_set():
            try:
                self.read_serial()
            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
            except Exception as e:
                exit(e)
            finally:
                try:
                    self.ser.close()
                except AttributeError:
                    pass
        # print("You exited!")

    def shutdown(self):
        """Shut down process."""
        self.exit.set()

    def init_serial(self):
        """Init serial port."""
        # Can't put it in init otherwise makes an error...
        self.ser = Serial(self.serial_port, timeout=None, baudrate=38400)

        self.pattern = re.compile(r'[\t\r\n]+')
        msg1 = 'My name is Arduinozaure. Send [ok] to start. Number of analogic pins: 6'
        msg2 = 'You can now ask a sensor value. Send me its pin number.'

        self.ser.read(self.ser.inWaiting())
        datas = re.sub(self.pattern, '', self.ser.readline().decode())
        while datas != msg1:
            time.sleep(0.4)
            datas = re.sub(self.pattern, '', self.ser.readline().decode())
        while datas != msg2:
            self.ser.read(self.ser.inWaiting())
            self.ser.write("ok".encode())
            time.sleep(0.4)
            datas = re.sub(self.pattern, '', self.ser.readline().decode())

    def read_serial(self):
        """Read serial port."""

        try:
            while not self.exit.is_set():
                self.get_port_list()
                for port in dict(self.ports):
                    self.ser.write(str.encode(str(port)))
                    data = re.sub(self.pattern, '',
                                  self.ser.readline().decode())
                    if self.sensors[port] is not None:
                        self.value[port] = self.sensors[port].transform_datas(
                            data)
                    else:
                        self.value[port] = data
                self.parent.set_datas(self.serial_port, dict(self.value))
        except (KeyboardInterrupt) as e:
            exit()
