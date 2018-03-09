"""Logging process."""
import json
import sys
import time
from multiprocessing import Event, Manager, Process

from .serialReader import SerialReader


class SerialManager(Process):
    """Process class."""

    def __init__(self):
        """Init process."""
        Process.__init__(self)
        self.name = "Fucking manager"
        self.exit = Event()
        self.serial_readers = {}
        print("Manager inited")
        sys.stdout.flush()
        self.datas = Manager().dict()

    def set_datas(self, port, datas):
        """Set data from child process."""
        self.datas[port] = json.dumps(datas)

    def get_serial_reader(self, port):
        """Get datas for specified serial port."""
        if port not in self.serial_readers:
            self.serial_readers[port] = SerialReader(port, self)
            self.serial_readers[port].start()

    def get_datas_for_port(self, port):
        """Get datas for serial port."""
        self.get_serial_reader(port)
        try:
            return self.datas[port]
        except KeyError:
            self.datas[port] = 'Initializing reader'
            return self.datas[port]

    def run(self):
        """Run process."""
        while not self.exit.is_set():
            try:
                # print("Manager running")
                sys.stdout.flush()
                time.sleep(0.5)
            except (KeyboardInterrupt, RuntimeError) as e:
                self.shutdown()
            except Exception as e:
                raise e
            finally:
                for s_r in self.serial_readers:
                    self.serial_readers[s_r].join()
        print("Manager exited")
        sys.stdout.flush()

    def shutdown(self):
        """Shut down process."""
        self.exit.set()
