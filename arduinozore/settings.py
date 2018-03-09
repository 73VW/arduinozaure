"""Settings module."""
import os


def path(root, *a):
    """Build path from root."""
    return os.path.join(root, *a)


ROOT = os.path.dirname(
    os.path.abspath(__file__))

TEMPLATE_FOLDER = path(ROOT, 'templates/')
CERT_FOLDER = path(ROOT, 'certs/')
STATIC_PATH = path(ROOT, 'static/')

SSL_PORT = 443

ssl_opts = {
    "certfile": path(CERT_FOLDER, "myserver.crt.pem"),
    "keyfile": path(CERT_FOLDER, "myserver.crt.key"),
}

settings = {'debug': True,
            'static_path': STATIC_PATH}

CONFIG_FOLDER = path(ROOT, '.config')
DEVICE_CONFIG_FOLDER = path(CONFIG_FOLDER, 'device')
CARDS = dict()
CARDS['UNO'] = dict()
CARDS['UNO']['NB_PINS'] = 6
