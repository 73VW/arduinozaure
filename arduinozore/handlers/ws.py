"""WebSocket handler package."""
import sys
from multiprocessing import Process

import sensors
from tornado.websocket import WebSocketHandler


class WSHandler(WebSocketHandler):
    """WebSocket handler."""

    clients = []
    serial_manager = None

    def __init__(self, *args, **kwargs):
        """Init handler."""
        WSHandler.serial_manager = kwargs.pop('serial_manager')
        super(WSHandler, self).__init__(*args, **kwargs)
        print("WSHandler inited")
        sys.stdout.flush()

    def check_origin(self, origin):
        """Check origin."""
        return True

    def get_serial_reader(self, name):
        """Return serial reader and creates it if it doesn't exists."""
        if name not in WSHandler.serial_readers:
            WSHandler.serial_readers[name] = Process(
                target=self.read_serial, args=(name,))
        return WSHandler.serial_readers[name]

    def open(self, slug):
        """Handle connection opening."""
        print('New connection was opened')
        """if not serial_reader.is_alive():
            serial_reader.start()"""
        sys.stdout.flush()
        self.port = slug
        self.write_message("Welcome to my websocket!")
        self.write_message(f'serial used: {slug}')
        datas = WSHandler.serial_manager.get_datas_for_port(slug)
        self.write_message(datas)
        self.sensor = sensors.Sensor("Sensor 1")
        WSHandler.clients.append(self)

    def on_message(self, message):
        """Handle incomming messages."""
        if message is not "Capteurs":
            sens_name = self.sensor.name
            class_ = getattr(sensors, message)
            self.sensor = class_(sens_name)

    def on_close(self):
        """Handle connection closing."""
        try:
            self.ser.close()
        except AttributeError:
            pass
        print('Connection was closed...')
        sys.stdout.flush()
        WSHandler.clients.remove(self)

    @classmethod
    def write_to_clients(cls):
        """Send message to all clients."""
        for client in cls.clients:
            datas = WSHandler.serial_manager.get_datas_for_port(client.port)
            client.write_message(datas)
