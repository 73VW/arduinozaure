"""Index page handler package."""
import socket

import tornado.web
from sensors import get_classes
from settings import TEMPLATE_FOLDER


class IndexPageHandler(tornado.web.RequestHandler):
    """Index page handler."""

    def __init__(self, *args, **kwargs):
        """Init handler."""
        s_p = kwargs.pop('ssl_port')
        self.ssl_port = s_p
        super(IndexPageHandler, self).__init__(*args, **kwargs)

    def get_template_path(self):
        """Get template path in order to find template files."""
        return TEMPLATE_FOLDER

    def prepare(self):
        """Prepare requests."""
        if self.request.protocol == 'http':
            self.redirect('https://' + self.request.host, permanent=False)

    def get(self):
        """Handle get request."""
        the_host = socket.gethostname()
        classes = get_classes()
        self.render('card.html', host=the_host,
                    port=self.ssl_port, items=classes)

    def set_default_headers(self, *args, **kwargs):
        """Set default headers."""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.set_header("Strict-Transport-Security",
                        "max-age=500; includeSubDomains; preload")
