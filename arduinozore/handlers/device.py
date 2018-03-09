"""Index page handler package."""
import socket

from sensors import get_classes
from settings import SSL_PORT

from .baseHandler import BaseHandler
from .tools import get_arduino, load_config_from_arduino


class DevicePageHandler(BaseHandler):
    """Device page handler."""

    def get(self, slug):
        """Handle get request."""
        arduino = get_arduino(slug)
        if arduino is not None:
            (device_name, ports) = load_config_from_arduino(arduino)
            if ports is not None and device_name is not None:
                the_host = socket.gethostname()
                classes = get_classes()
                self.render('device.html',
                            host=the_host,
                            port=SSL_PORT,
                            items=classes,
                            slug=slug,
                            device=device_name,
                            ports=ports)
            else:
                self.redirect('https://' + self.request.host +
                              self.request.uri.rstrip("/") + '/edit', permanent=False)
        else:
            self.render("404.html")
