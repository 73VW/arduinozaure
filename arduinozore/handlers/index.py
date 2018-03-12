"""Index page handler package."""

from .baseHandler import BaseHandler
from .tools import get_arduinos
from models.device import Device


class IndexPageHandler(BaseHandler):
    """Index page handler."""

    def get(self):
        """Handle get request."""
        devices = Device.get_connected_devices()
        self.render('index.html', devices=devices)
