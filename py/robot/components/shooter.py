import wpilib
from ctre import WPI_TalonFX
from wpilib import DoubleSolenoid
import ctre


class Shooter:

    motor_master = WPI_TalonFX
    motor_slave = WPI_TalonFX
    hood_solenoid = DoubleSolenoid

    state = False

    value = DoubleSolenoid.Value.kForward

    def setup(self):
        #shooter
        self.speed=0.0

        #set slave motor
        #self.motor_slave.set(ctre.TalonFXControlMode.Follower, self.motor_master.getDeviceID())
        self.motor_master.setInverted(True)

        #hood
        self.value = DoubleSolenoid.Value.kForward
        self.state = False

    def run_shooter(self, speed):
        self.motor_master.set(speed)
        self.motor_slave.set(speed)
        self.speed = speed
    
    def switch(self):
        print("switch")
        if self.state == False:
            self.state = True
            self.value = DoubleSolenoid.Value.kReverse
        elif self.state == True:
            self.state = False
            self.value = DoubleSolenoid.Value.kForward

    def extend(self):
        self.state = True

    def retract(self):
        self.state = False

    def get_state(self):
        return {
            'hood_state': self.state,
        }

    def execute(self):
        print("execute")
        if self.state == True:
            self.hood_solenoid.set(self.value)
        elif self.state == False:
            self.hood_solenoid.set(self.value)

        if self.enable:
            self.run_shooter(self.speed)
        else:
            self.run_shooter(0)
