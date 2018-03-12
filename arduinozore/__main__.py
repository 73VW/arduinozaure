"""Arduinozore module."""

import socket
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from handlers.error404handler import My404Handler
from handlers.serialManager import SerialManager
from handlers.ws import WSHandler
from settings import SSL_PORT
from settings import settings
from settings import ssl_opts
from urls import url_pattern


def main():
    """Catch main function."""
    serial_manager = SerialManager()
    try:
        serial_manager.start()
        url_pattern[-1] = (*url_pattern[-1],
                           {'serial_manager': serial_manager})
        index_application = tornado.web.Application(
            url_pattern, default_handler_class=My404Handler, **settings)

        index_application.listen(80)
        http_server = tornado.httpserver.HTTPServer(
            index_application,
            ssl_options=ssl_opts
        )
        http_server.listen(SSL_PORT)
        tornado.ioloop.PeriodicCallback(WSHandler.write_to_clients, 500).start()
        print("Listening on : https://" + str(socket.gethostname()))
        sys.stdout.flush()
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        exit(e)
    finally:
        serial_manager.join()


if __name__ == "__main__":
    main()
