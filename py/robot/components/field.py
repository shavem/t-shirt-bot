from enum import IntEnum
import wpilib
from networktables import NetworkTables


class Field:

    def execute(self):
        robot_table = NetworkTables.getTable('robot')
        robot_table.putValue('time', wpilib.Timer.getMatchTime())
