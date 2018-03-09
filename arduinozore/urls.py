"""Urls module."""
from handlers.device import DevicePageHandler
from handlers.device_config import DeviceConfigHandler
from handlers.index import IndexPageHandler
from handlers.ws import WSHandler
from settings import STATIC_PATH
from tornado.web import StaticFileHandler

url_pattern = [
    (r'/static/(.*)', StaticFileHandler, {'path': STATIC_PATH}),
    (r'/', IndexPageHandler),
    (r'/device/([^/]+)/edit', DeviceConfigHandler),
    (r'/device/([^/]+)', DevicePageHandler),
    (r'/ws/([^/]+)', WSHandler),  # always the last one!
]
