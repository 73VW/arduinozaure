"""Sensor module."""
import os
import ast


def get_classes():
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

    def transform_datas(self, raw_datas):
        """Transform datas read from COM port to a human readle value."""
        return str(int(float(raw_datas) * 10))


class TestSensor(Sensor):

    def transform_datas(self, raw_datas):
        """Transform datas read from COM port to a human readle value."""
        return str(int(float(raw_datas) * 1000))


if __name__ == "__main__":
    print(get_classes())
