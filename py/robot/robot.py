import wpilib
import ctre
import magicbot
import wpilib.drive
from wpilib import Solenoid, DoubleSolenoid



'''python py/robot/robot.py deploy --skip-tests'''

'''py -3 -m pip install -U robotpy[ctre]'''


'''
NetworkTables.initialize(server=x'roborio-5045-frc.local')

sd = NetworkTables.getTable('SmartDashboard')
sd.putNumber('someNumber', 1234)
otherNumber = sd.getNumber('otherNumber')


# ./py/venv/Scripts/activate
'''

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand

class SpartaBot(magicbot.MagicRobot):

    def createObjects(self):
        self.compressor = wpilib.Compressor()
        self.solenoidp1 = wpilib.Solenoid(0)
        self.solenoidp2 = wpilib.Solenoid(1)
        # self.solenoid = wpilib.DoubleSolenoid(0, 1)
        self.shift_toggle1 = DoubleSolenoid.Value.kForward
        self.shift_toggle2 = DoubleSolenoid.Value.kReverse

        self.drive_controller = wpilib.XboxController(1)

        # drivetrain
        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(3)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(4)
        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(1)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(2)
        self.left = wpilib.SpeedControllerGroup(
            self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave)
        self.right = wpilib.SpeedControllerGroup(
            self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        # shooter
        self.shooter_motor_master = ctre.WPI_TalonSRX(5)
        self.shooter_motor_slave = ctre.WPI_TalonSRX(6)


        # wpilib.CameraServer.launch()

    def autonomousInit(self):
        # self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        # self.intake_arm_solenoid.set(DoubleSolenoid.Value.kReverse)
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass
        # self.drive.setSafetyEnabled(True)
        # self.drive.setSafetyEnabled(False)

    def teleopPeriodic(self):

        # Solenoid test
        if self.drive_controller.getBButtonReleased():
            self.solenoidp1.set(self.shift_toggle1)
            self.solenoidp2.set(self.shift_toggle2)
            if (self.shift_toggle1 == DoubleSolenoid.Value.kForward):
                self.shift_toggle1 = DoubleSolenoid.Value.kReverse
                self.shift_toggle2 = DoubleSolenoid.Value.kForward
            else:
                self.shift_toggle1 = DoubleSolenoid.Value.kForward
                self.shift_toggle2 = DoubleSolenoid.Value.kReverse


        angle = self.drive_controller.getX(CONTROLLER_RIGHT)
        speed = self.drive_controller.getY(CONTROLLER_LEFT)
        if (abs(angle) > 0.08 or abs(speed) > 0.08):
            self.drive.arcadeDrive(-speed, -angle, True)
        else:
            self.drive.arcadeDrive(0, 0, True)


        # shooter
        if self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT) > 0.01:
            self.shooter_motor_master.set(-(self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT)))
            self.shooter_motor_slave.set(-self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT))
            # print("Shooter speed: " + str(self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT)))
        elif self.drive_controller.getTriggerAxis(CONTROLLER_LEFT) > 0.01:
            self.shooter_motor_master.set(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))
            self.shooter_motor_slave.set(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))
            # print("Shooter speed: " + str(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT)))
        else:
            self.shooter_motor_master.set(0)
            self.shooter_motor_slave.set(0)



        # if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
        #     self.shifter_shiftsolenoid.set(False)
        # if self.drive_controller.getStickButtonReleased(CONTROLLER_RIGHT):
        #     self.shifter_shiftsolenoid.set(True)


if __name__ == '__main__':
    wpilib.run(SpartaBot)