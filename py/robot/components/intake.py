from ctre import WPI_TalonSRX
from magicbot import tunable
from enum import IntEnum
from wpilib import DoubleSolenoid
from constants import TALON_TIMEOUT

class IntakeState(IntEnum):
    EXTENDED = 0
    RETRACTED = 1


class Intake:
    roller_motor = WPI_TalonSRX
    arm_solenoid = DoubleSolenoid

    def setup(self):
        self.state = IntakeState.RETRACTED
        self.roller_motor.setInverted(True)
        self.roller_motor.setSensorPhase(True)

        self.speed = 0.0

    def switch(self):
        if self.state == IntakeState.EXTENDED:
            self.state = IntakeState.RETRACTED
        elif self.state == IntakeState.RETRACTED:
            self.state = IntakeState.EXTENDED

    def extend(self):
        self.state = IntakeState.EXTENDED

    def retract(self):
        self.state = IntakeState.RETRACTED

    def run_roller(self, speed):
        self.roller_motor.set(speed)
        

    def get_state(self):
        return {
            'arm_state': self.state,
        }

    def execute(self):
        if self.state == IntakeState.RETRACTED:
            self.arm_solenoid.set(DoubleSolenoid.Value.kForward)
            self.run_roller(self.speed)
        elif self.state == IntakeState.EXTENDED:
            self.arm_solenoid.set(DoubleSolenoid.Value.kReverse)
            self.roller_motor.stopMotor()
        else:
            self.roller_motor.stopMotor()
    