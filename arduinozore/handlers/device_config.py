"""Index page handler package."""
import re

from settings import CARDS, DEVICE_CONFIG_FOLDER, path
from yaml import dump

from .baseHandler import BaseHandler
from .tools import get_arduino, load_config_from_arduino


class DeviceConfigHandler(BaseHandler):
    """Device page handler."""

    def get(self, slug):
        """Handle get request."""
        arduino = get_arduino(slug)
        if arduino is not None:
            (device_name, ports) = load_config_from_arduino(arduino)
            settings = dict()
            if ports is not None and device_name is not None:
                settings['device_name'] = device_name
                settings['device'] = slug
                settings['ports'] = ports
                settings['nb_ports'] = CARDS['UNO']['NB_PINS']
            else:
                settings['device_name'] = ""
                settings['device'] = slug
                settings['ports'] = dict()
                settings['nb_ports'] = CARDS['UNO']['NB_PINS']

            self.render('device_config.html', **settings)
        else:
            self.render("404.html")

    def post(self, slug):
        """Handle post request."""
        arduino = get_arduino(slug)
        config_name = f'{arduino.vid}{arduino.pid}{arduino.serial_number}'
        config_name += ".yaml"
        config_name = path(DEVICE_CONFIG_FOLDER, config_name)
        args = dict()
        default_args = dict()
        default_args['enabled'] = ''
        default_args['name'] = ''
        default_args['type'] = ''
        pattern = re.compile(r'[\[\]]+')
        for i in range(CARDS['UNO']['NB_PINS']):
            p = f'port{i}'
            args[i] = {re.sub(pattern, '',  k.strip(p)): self.get_argument(
                k) for k in self.request.arguments if p in k}
            if len(args[i]) is 0:
                args[i] = dict(default_args)
        device_name = self.get_argument('device-name')
        if device_name == "":
            self.render('device_config.html', device=slug,
                        device_name=device_name, port_list="")
            return
        datas = {'device_name': device_name, 'ports': args}
        with open(config_name, 'w') as f:
            d = dump(datas, default_flow_style=False,
                     allow_unicode=True, encoding=None)
            f.write(d)

        self.redirect('https://' + self.request.host +
                      self.request.uri.rstrip('/edit'), permanent=True)
