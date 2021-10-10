from wpilib import SerialPort, AnalogInput, AnalogOutput, I2C
from magicbot import tunable
from math import degrees, atan2
from networktables import NetworkTables
import re

IR_SEPARATION = 128
table = NetworkTables.getTable('components/irsensor')

class IRSensor:

    serial = SerialPort
    i2c = I2C
    threshold = tunable(300)

    def setup(self):
        self.activations = None
        self.angle = None
        self.displacement = None
        self.oriented = False
        self.saved_threshold = 300
        
    def set_threshold(self):
        self.serial.writeString("t"+str(self.threshold))
        return self.serial.readString(3)==str(self.threshold)

    def get_array_one(self):
        a = str(bin(0))[2:] 
        b = str(bin(0))[2:]
        return a+'0'*(10-len(a))+b+'0'*(10-len(b))

    def get_array_two(self):
        a = str(bin(0))[2:] 
        b = str(bin(0))[2:]
        return a+'0'*(10-len(a))+b+'0'*(10-len(b))
        
    def compute_orientation(self):
        c1 = [i for i,j in enumerate(self.activations[:16]) if int(j)]
        c1 = sum(c1)/(len(c1)+0.01)
        c2 = [i for i,j in enumerate(self.activations[16:]) if int(j)]
        c2 = sum(c2)/(len(c2)+0.01)

        self.displacement = 62.5 - (8*c1+8*c2)/2
        self.angle = degrees(atan2(c1-62.5,IR_SEPARATION/2))

    def isOriented(self):
        return self.oriented

    def execute(self):
        if self.saved_threshold != self.threshold:
            success = self.set_threshold()
            if success:
                self.saved_threshold = self.threshold
            else:
                self.threshold = self.saved_threshold
        self.activations = self.get_array_one()+self.get_array_two()
        self.compute_orientation()
        table.putValue('activations', self.activations)
        table.putValue('angle', self.activations)
        table.putValue('displacement', self.activations)
