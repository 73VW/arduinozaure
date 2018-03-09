"""404 error handling package."""
from settings import TEMPLATE_FOLDER

from .baseHandler import BaseHandler


class My404Handler(BaseHandler):
    """404 error handler."""

    def get_template_path(self):
        """Get template path in order to find template files."""
        return TEMPLATE_FOLDER

    def prepare(self):
        """Override prepare to cover all possible HTTP methods."""
        if self.request.protocol == 'http':
            self.redirect('https://' + self.request.host +
                          self.request.uri, permanent=False)
        self.set_status(404)
        self.render("404.html")
