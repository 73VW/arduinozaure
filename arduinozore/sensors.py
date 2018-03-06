"""Sensor module."""
import ast
import os


def get_classes():
    """Get classes contained in this file."""
    filename = os.path.basename(__file__)
    with open(filename) as file:
        node = ast.parse(file.read())

    classes = [n.name for n in node.body if isinstance(n, ast.ClassDef)]
    return classes


class Sensor:
    """Sensor class."""

    def __init__(self, name):
        """Init sensor."""
        self.name = name

    def get_datas(self, raw_datas):
        """Get datas transformed from raw_datas."""
        try:
            return self.transform_datas(raw_datas)
        except Exception as e:
            return "Can't fetch value: " + raw_datas

    def transform_datas(self, raw_datas):
        """Transform datas read from COM port to a human readle value."""
        return str(int(float(raw_datas) * 10))


class TestSensor(Sensor):
    """TestSensor class."""

    def transform_datas(self, raw_datas):
        """Transform datas read from COM port to a human readle value."""
        return str(int(float(raw_datas) * 1000))


class KY028(Sensor):
    """KY028 Sensor class."""

    def transform_datas(self, raw_datas):
        """Transform datas read from COM port to a human readle value."""
        d = float(raw_datas)
        return str(round((d / 1024 * (-180) + 125), 1)) + "°C"


if __name__ == "__main__":
    print(get_classes())
