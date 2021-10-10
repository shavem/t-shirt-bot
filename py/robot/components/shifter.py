import wpilib
from enum import IntEnum
from wpilib import Solenoid


class Shifter:

    shiftsolenoid = Solenoid

    def setup(self):
        self.pending_gear = False

    def shift_low_gear(self):
        self.pending_gear = False

    def shift_high_gear(self):
        self.pending_gear = True

    def shift_toggle(self):
        if self.pending_gear == True:
            self.pending_gear = False
        else:
            self.pending_gear = True
    
    def execute(self):
        # Shifter
        self.shiftsolenoid.set(self.pending_gear)
