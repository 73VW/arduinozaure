"""Arduinozore module."""
import sys
import time
from multiprocessing import Process, Queue

import serial
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from handlers.ws.WSHandler import write_to_clients
from settings import SSL_PORT, settings, ssl_opts
from urls import url_pattern


def main():
    """Catch main function."""
    q = Queue()
    p = Process(target=read_serial, args=(q, ))
    try:

        p.start()
        url_pattern[1] = (*url_pattern[1], {"ssl_port": SSL_PORT})
        url_pattern[2] = (*url_pattern[2], {"q": q})
        index_application = tornado.web.Application(url_pattern, **settings)

        index_application.listen(80)
        http_server = tornado.httpserver.HTTPServer(
            index_application,
            ssl_options=ssl_opts
        )
        http_server.listen(SSL_PORT)
        tornado.ioloop.PeriodicCallback(write_to_clients, 500).start()
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        exit(e)
    finally:
        p.join()
        pass


def read_serial(q):
    """Read serial port."""
    ser = serial.Serial('COM20', timeout=None)

    ser.read(ser.inWaiting())
    time.sleep(0.5)
    ser.readline()
    ser.write(str.encode("ok"))
    ser.readline().decode()
    time.sleep(0.3)
    try:
        while(True):
            time.sleep(0.1)
            ser.write(str.encode(str(5)))
            data = ser.read_until(b'\x0D', 1000)
            data_str = data.decode()
            data_str = data_str.strip("\r")
            q.put(data_str)
            print("Put: " + data_str)
            sys.stdout.flush()
    except (Exception, KeyboardInterrupt) as e:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    main()
