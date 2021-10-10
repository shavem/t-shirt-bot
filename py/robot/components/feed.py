import wpilib
from ctre import WPI_TalonSRX

class Feed:

    motor_master = WPI_TalonSRX
    motor_slave = WPI_TalonSRX

    def setup(self):
        #feed
        self.speed=0.0

        #set slave motor
        self.motor_slave.set(WPI_TalonSRX.ControlMode.Follower,
                                  self.motor_master.getDeviceID())

    def run_feed(self, speed):
        self.motor_master.set(speed)
        self.speed = speed
    
    def execute(self):
        self.run_feed(self.speed)
