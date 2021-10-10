from ctre import WPI_TalonSRX
from magicbot import tunable
from enum import IntEnum
from wpilib import DoubleSolenoid
from constants import TALON_TIMEOUT

class ClawState(IntEnum):
    EXTENDED = 0
    RETRACTED = 1

class ShiftState(IntEnum):
    EXTENDED = 0
    RETRACTED = 1

class Manipulator:

    belt_motor = WPI_TalonSRX
    roller_motor = WPI_TalonSRX
    solenoid = DoubleSolenoid
    shift = DoubleSolenoid
    
    def setup(self):
        self.state = ClawState.RETRACTED
        self.shift_state = ShiftState.RETRACTED
        self.belt_motor.setSensorPhase(True)
        self.roller_motor.setInverted(True)
        self.roller_motor.setSensorPhase(True)

        self.speed = 0.0

    def switch(self):
        if self.state == ClawState.EXTENDED:
            self.state = ClawState.RETRACTED
        elif self.state == ClawState.RETRACTED:
            self.state = ClawState.EXTENDED

    def extend(self):
        self.state = ClawState.EXTENDED

    def retract(self):
        self.state = ClawState.RETRACTED

    def run_belt(self, speed):
        self.belt_motor.set(speed)

    def run_roller(self, speed):
        self.roller_motor.set(speed)
    
    def shift_pad(self):
        if self.shift_state == ShiftState.EXTENDED:
            self.shift_state = ShiftState.RETRACTED
        elif self.shift_state == ShiftState.RETRACTED:
            self.shift_state = ShiftState.EXTENDED


    def get_state(self):
        return {
            'claw_state': self.state,
            'shift_state': self.shift_state
        }

    def put_state(self, state):
        self.state = state['claw_state']
        self.shift_state = state['shift_state']

    def execute(self):
        if self.state == ClawState.RETRACTED:
            self.solenoid.set(DoubleSolenoid.Value.kForward)
        elif self.state == ClawState.EXTENDED:
            self.solenoid.set(DoubleSolenoid.Value.kReverse)

        if self.shift_state == ShiftState.RETRACTED:
            self.shift.set(DoubleSolenoid.Value.kForward)
        elif self.shift_state == ShiftState.EXTENDED:
            self.shift.set(DoubleSolenoid.Value.kReverse)

        self.run_belt(self.speed)
        self.run_roller(self.speed)
