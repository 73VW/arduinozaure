import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import serial
import io
import sys
import datetime
import os

import sensors
from sensors import get_classes

ser = serial.Serial('COM18', timeout=None)

port_socket = 8888


class IndexPageHandler(tornado.web.RequestHandler):

    def prepare(self):
        if self.request.protocol == 'http':
            self.redirect('https://' + self.request.host, permanent=False)

    def get(self):
        the_host = socket.gethostname()
        classes = get_classes()
        self.render("./index.html", host=the_host,
                    port=port_socket, items=classes)

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.set_header("Strict-Transport-Security",
                        "max-age=500; includeSubDomains; preload")


class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True

    def open(self):
        print('New connection was opened')
        sys.stdout.flush()
        self.write_message("Welcome to my websocket!")
        self.ser = ser
        self.sensor = sensors.Sensor("Sensor 1")
        WSHandler.clients.append(self)

    def on_message(self, message):
        if message is not "Capteurs":
            sens_name = self.sensor.name
            class_ = getattr(sensors, message)
            self.sensor = class_(sens_name)

    def on_close(self):
        print('Connection was closed...')
        WSHandler.clients.remove(self)

    @classmethod
    def write_to_clients(cls):
        if ser.is_open and ser.inWaiting() > 0:
            data = ser.read_until(b'\x0D', 1000)
            data_str = data.decode()
            data_str = data_str.strip("\r")
            if data_str is not "":
                for client in cls.clients:
                    print("Writing to clients")
                    sys.stdout.flush()
                    client.write_message(
                        client.sensor.transform_datas(data_str))


ws_application = tornado.web.Application([
    (r'/ws', WSHandler),
])

index_application = tornado.web.Application([
    (r'/semantic/(.*)',
     tornado.web.StaticFileHandler,
     {'path': './semantic'}),
    (r'/', IndexPageHandler),
])

ssl_opts = {
    "certfile": os.path.join("certs/", "myserver.crt.pem"),
    "keyfile": os.path.join("certs/", "myserver.crt.key"),
}

if __name__ == "__main__":
    try:
        ws_server = tornado.httpserver.HTTPServer(
            ws_application, ssl_options=ssl_opts)
        ws_server.listen(port_socket)

        index_application.listen(80)
        http_server = tornado.httpserver.HTTPServer(
            index_application,
            ssl_options=ssl_opts
        )
        http_server.listen(443)
        tornado.ioloop.PeriodicCallback(WSHandler.write_to_clients, 500).start()
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        print(e)
        ser.close()
