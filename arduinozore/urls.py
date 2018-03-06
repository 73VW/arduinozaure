"""Urls module."""
from handlers.index_page import IndexPageHandler
from handlers.ws import WSHandler
from settings import STATIC_PATH
from tornado.web import StaticFileHandler

url_pattern = [
    (r'/static/(.*)', StaticFileHandler, {'path': STATIC_PATH}),
    (r'/', IndexPageHandler),
    (r'/ws', WSHandler),
]
