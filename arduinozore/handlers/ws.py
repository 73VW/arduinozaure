"""WebSocket handler package."""
import sys

import sensors
import tornado.websocket


class WSHandler(tornado.websocket.WebSocketHandler):
    """WebSocket handler."""

    clients = []
    queue = None

    def __init__(self, *args, **kwargs):
        """Init handler."""
        q = kwargs.pop('q')
        WSHandler.queue = q
        super(WSHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        """Check origin."""
        return True

    def open(self):
        """Handle connection opening."""
        print('New connection was opened')
        sys.stdout.flush()
        self.write_message("Welcome to my websocket!")
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
        print('Connection was closed...')
        WSHandler.clients.remove(self)

    @classmethod
    def write_to_clients(cls):
        """Send message to all clients."""
        if cls.queue is not None and not cls.queue.empty():
            data_str = cls.queue.get()
            if data_str is not "":
                for client in cls.clients:
                    print("Writing to clients")
                    sys.stdout.flush()
                    client.write_message(client.sensor.get_datas(data_str))
