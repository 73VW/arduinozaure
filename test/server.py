import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
#import RPi.GPIO as GPIO

REDPIN = 15
WHITEPIN = 14

red_state = 0
white_state = 0

port_socket = 8888
port_index = 80


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        the_host = socket.gethostname()
        self.render("./index.html", host=the_host, port=port_socket)


class WSHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)
        print('New connection was opened')
        self.write_message("Welcome to my websocket!")

    def on_message(self, message):
        print('Incoming message:', message)
        [con.write_message(message) for con in self.connections]

    def on_close(self):
        print('Connection was closed...')


ws_application = tornado.web.Application([
    (r'/ws', WSHandler),
])

index_application = tornado.web.Application([
    (r'/semantic/(.*)',
     tornado.web.StaticFileHandler,
     {'path': './semantic'}),
    (r'/', IndexPageHandler),
])

if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(ws_application)
        http_server.listen(port_socket)

        http_server2 = tornado.httpserver.HTTPServer(index_application)
        http_server2.listen(port_index)

        tornado.ioloop.IOLoop.instance().start()
    except:
        pass
