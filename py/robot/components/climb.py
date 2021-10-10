import wpilib
from ctre import WPI_TalonSRX

class Climb:
    
    motor_master = WPI_TalonSRX
    motor_slave = WPI_TalonSRX

    def setup(self):
        self.speed=0.0
        #set slave motor
        self.motor_slave.set(WPI_TalonSRX.ControlMode.Follower, self.motor_master.getDeviceID())

    def run_shooter(self, speed):
        self.motor_master.set(speed)


    def execute(self):
        self.run_shooter(self.speed)