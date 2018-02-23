#!/usr/bin/env python

import os
import tornado.httpserver
import tornado.web
import tornado.ioloop


class MainHandler(tornado.web.RequestHandler):

    def prepare(self):
        if self.request.protocol == 'http':
            self.redirect('https://' + self.request.host, permanent=False)

    def get(self):
        self.write("Hello, world")


ssl_opts = {
    "certfile": os.path.join("certs/", "myserver.crt.pem"),
    "keyfile": os.path.join("certs/", "myserver.crt.key"),
}

if __name__ == "__main__":
    application = tornado.web.Application([
        (r'/', MainHandler)
    ])
    application.listen(80)
    http_server = tornado.httpserver.HTTPServer(
        application,
        ssl_options=ssl_opts
    )
    http_server.listen(443)
    tornado.ioloop.IOLoop.current().start()
