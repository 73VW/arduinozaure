"""Index page handler package."""

from .baseHandler import BaseHandler
from .tools import get_arduinos


class IndexPageHandler(BaseHandler):
    """Index page handler."""

    def get(self):
        """Handle get request."""
        arduinos = get_arduinos()
        self.render('index.html', arduinos=arduinos)
