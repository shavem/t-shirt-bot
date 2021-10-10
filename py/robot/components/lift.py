from ctre import WPI_TalonSRX
from magicbot import tunable
from enum import IntEnum
from wpilib import DoubleSolenoid


class LiftState(IntEnum):
    RETRACTED = 0
    EXTENDED = 1


class Lift:

    belt_motor = WPI_TalonSRX
    roller_motor = WPI_TalonSRX
    solenoid = DoubleSolenoid

    def setup(self):
        self.state = LiftState.RETRACTED
        
    def switch(self):
        if self.state == LiftState.EXTENDED:
            self.state = LiftState.RETRACTED
        elif self.state == LiftState.RETRACTED:
            self.state = LiftState.EXTENDED

    def extend(self):
        self.state = LiftState.EXTENDED

    def retract(self):
        self.state = LiftState.RETRACTED

    def get_state(self):
        return {
            'lift_state': self.state
        }

    def put_state(self, state):
        self.state = state['lift_state']

    def execute(self):
        if self.state == LiftState.RETRACTED:
            self.solenoid.set(DoubleSolenoid.Value.kReverse)
        elif self.state == LiftState.EXTENDED:
            self.solenoid.set(DoubleSolenoid.Value.kForward)
