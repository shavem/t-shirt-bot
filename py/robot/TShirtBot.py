import wpilib
import ctre
import magicbot
import wpilib.drive
from wpilib import Solenoid, DoubleSolenoid
import drivetrain, shooter

'''python py/robot/TShirtBot.py deploy --skip-tests'''



CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand


class SpartaBot(magicbot.MagicRobot):
    def createObjects(self):

        self.drive_controller = wpilib.XboxController(0)
        # self.compressor = wpilib.Compressor()

        # drivetrain
        self.drivetrain = drivetrain.Drivetrain
        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(4)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(3)

        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(1)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(2)

        # shooter
        self.shooter = shooter.Shooter
        # self.shooter_motor = ctre.WPI_TalonSRX(5)
        self.shooter_motor_master = ctre.WPI_TalonSRX(5)
        self.shooter_motor_slave = ctre.WPI_TalonSRX(6)

    def autonomousInit(self):
        # self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        # self.intake_arm_solenoid.set(DoubleSolenoid.Value.kReverse)
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        # drivetrain
        angle = self.drive_controller.getX(CONTROLLER_RIGHT)
        speed = self.drive_controller.getY(CONTROLLER_LEFT)
        self.drivetrain.angle_corrected_differential_drive(self.drive_controller.getY(CONTROLLER_LEFT), angle)

        # shooter
        if self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT) > 0.9:
            self.shooter_motor_master.set(0.9)
            self.shooter_motor_slave.set(-0.9)
        elif self.drive_controller.getBButton():
            self.shooter_motor_master.set(0.5)
            self.shooter_motor_slave.set(-0.5)
        elif self.drive_controller.getBumper(CONTROLLER_RIGHT):
            self.shooter_motor_master.set(0.35)
            self.shooter_motor_slave.set(-0.35)
        else:
            self.shooter_motor_master.set(0)
            self.shooter_motor_slave.set(0)
        if self.drive_controller.getXButtonReleased():
            self.shooter.switch()
        if self.drive_controller.getStartButtonReleased():
            self.drivetrain_right_motor_master.set(0.1)


if __name__ == '__main__':
    wpilib.run(SpartaBot)