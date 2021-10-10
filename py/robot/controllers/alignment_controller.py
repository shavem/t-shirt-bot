from magicbot import tunable
from wpilib import PIDController
import hal
from networktables import NetworkTables

from components.drivetrain import Drivetrain
from components.targeting import Targeting


class AlignmentController:

    drivetrain = Drivetrain
    targeting = Targeting

    rate = .5
    kP = 0.05
    kI = 0
    kD = 0.005
    kF = 0

    def __init__(self):
        self.angle = None
        self.angle_pid_controller = PIDController(
            Kp=self.kP, Ki=self.kI, Kd=self.kD, Kf=self.kF,
            source=self.get_angle,
            output=self.pidWriteAngle)
        self.angle_pid_controller.setInputRange(-180, 180)
        self.angle_pid_controller.setContinuous(True)
        self.angle_pid_controller.setOutputRange(-self.rate,
                                                 self.rate)
        self.nt = NetworkTables.getTable('limelight')

    def get_position(self):
        return self.drivetrain.get_position()

    def get_angle(self):
        angle = self.targeting.get_data().x
        if angle!=0.0:
            self.angle = angle
        return self.angle

    def found(self):
        fnd = self.targeting.get_data().found
        if fnd == 1:
            return True
        else:
            return False

    def move_to(self, position):
        self.setpoint = position
        self.angle_pid_controller.enable()

    def pidWriteAngle(self, rate):
        self.rate = rate

    def execute(self):
        if self.rate is not None:
            if self.found():
                self.drivetrain.differential_drive(0)
                self.stop()
            else:
                self.drivetrain.manual_drive(-self.rate, self.rate)

    def stop(self):
        self.angle_pid_controller.disable()

    def on_disable(self):
        self.stop()
