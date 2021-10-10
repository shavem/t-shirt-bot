from collections import namedtuple
from networktables import NetworkTables

TargetingData = namedtuple('TargetingOffset',
                           ['found', 'x', 'y', 'area', 'skew'])

LED_MODE_ON = 0
LED_MODE_OFF = 1
LED_MODE_BLINK = 2

CAMERA_MODE_VISION = 0
CAMERA_MODE_DRIVER = 1


class Targeting:
    def setup(self):
        self.nt = NetworkTables.getTable('limelight')
        self.oriented = False

    def set_led_mode(self, mode):
        self.nt.setNumber('ledMode', mode)

    def set_camera_mode(self, mode):
        self.nt.setNumber('camMode', mode)

    def get_data(self):
        return TargetingData(found=self.nt.getNumber('tv', 0) == 1,
                             x=(self.nt.getNumber('tx', 0)),
                             y=(self.nt.getNumber('ty', 0)),
                             area=(self.nt.getNumber('ta', 0)),
                            skew=(self.nt.getNumber('ts', 0)))

    def isOriented(self):
        return self.oriented

    def execute(self):
        pass
