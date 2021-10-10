import wpilib
from ctre import WPI_TalonFX
from enum import IntEnum
from wpilib import DoubleSolenoid

class HoodState(IntEnum):
    EXTENDED = 0
    RETRACTED = 1

class Shooter:

    shooter_motor = WPI_TalonFX
    shooter_motor_slave = WPI_TalonFX
    hood_solenoid = DoubleSolenoid

    enabled = False
    executed = False

    def __init__(self):
        #shooter
        self.speed=0.0
        #self.shooter_motor.setInverted(True)

        #hood
        self.state = HoodState.RETRACTED


    def run_shooter(self, speed):
        self.speed = speed
        print (self.speed , "runshooter")
        self.enabled = True
        print (self.enabled , "runshooter")
        print (self.executed , "runshooter")

    def switch(self):
        if self.state == HoodState.EXTENDED:
            self.state = HoodState.RETRACTED
        elif self.state == HoodState.RETRACTED:
            self.state = HoodState.EXTENDED

    def extend(self):
        self.state = HoodState.EXTENDED

    def retract(self):
        self.state = HoodState.RETRACTED

    def get_state(self):
        return {
            'hood_state': self.state,
        }

    def execute(self):
        #hood
        '''
        if self.state == HoodState.RETRACTED:
            self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        elif self.state == HoodState.EXTENDED:
            self.hood_solenoid.set(DoubleSolenoid.Value.kReverse)
        '''

        #shooter
        print (self.speed , "execute")
        if self.enabled:
            self.shooter_motor.set(self.speed)
            self.shooter_motor_slave.set(-self.speed)
        else:
            self.shooter_motor.set(0)
            self.shooter_motor_slave.set(0)
        self.enabled = False
        self.executed = True
