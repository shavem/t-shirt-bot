import wpilib
import rev
import magicbot
import wpilib.drive
from networktables import NetworkTables
import logging
from wpilib import Solenoid, DoubleSolenoid
import time


# Push code to RoboRIO
'''python py/robot/robot.py deploy --skip-tests'''

# idrk what this does
'''py -3 -m pip install -U robotpy[ctre]'''
'''py -3 -m pip install robotpy[ctre]'''


# Download and install stuff on the RoboRIO after imaging
'''py -3 -m robotpy_installer download-python
   py -3 -m robotpy_installer install-python
   py -3 -m robotpy_installer download robotpy
   py -3 -m robotpy_installer install robotpy
   py -3 -m robotpy_installer download robotpy[ctre]
   py -3 -m robotpy_installer install robotpy[ctre]
   py -3 -m robotpy_installer download robotpy[rev]
   py -3 -m robotpy_installer install robotpy[rev]'''


'''
NetworkTables.initialize(server=x'roborio-5045-frc.local')

sd = NetworkTables.getTable('SmartDashboard')
sd.putNumber('someNumber', 1234)
otherNumber = sd.getNumber('otherNumber')


# ./py/venv/Scripts/activate
'''

# CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
# CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand
PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed
SPEED_MULTIPLIER = 0.8

class SpartaBot(magicbot.MagicRobot):

    def createObjects(self):

        # Initialize SmartDashboard
        logging.basicConfig(level=logging.DEBUG)
        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd = NetworkTables.getTable('SmartDashboard')



        # self.compressor = wpilib.Compressor(PNEUMATICS_MODULE_TYPE)
        # self.solenoidp1 = wpilib.Solenoid(0)
        # self.solenoidp2 = wpilib.Solenoid(1)
        # self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)
        # self.solenoid.set(DoubleSolenoid.Value.kReverse)
        # self.solenoidp1.set(True)
        # self.solenoidp2.set(True)

        self.drive_controller = wpilib.XboxController(1)

        # drivetrain
        # self.drivetrain_right_motor_master = rev.CANSparkMax(1, MOTOR_BRUSHED)
        # self.drivetrain_right_motor_slave = rev.CANSparkMax(2, MOTOR_BRUSHED)
        # self.drivetrain_left_motor_master = rev.CANSparkMax(3, MOTOR_BRUSHED)
        # self.drivetrain_left_motor_slave = rev.CANSparkMax(4, MOTOR_BRUSHED)
        # self.left = wpilib.SpeedControllerGroup(
        #     self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave)
        # self.right = wpilib.SpeedControllerGroup(
        #     self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave)
        # self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        # self.drive.setExpiration(0.1)

        # shooter
        self.shooter_motor_master = ctre.WPI_TalonSRX(3)
        self.shooter_motor_slave = ctre.WPI_TalonSRX(4)

        # Intake
        self.intake_motor = rev.CANSparkMax(1, MOTOR_BRUSHED)
        self.tower_motor = rev.CANSparkMax(2, MOTOR_BRUSHED)


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
        # if self.drive_controller.getBButtonReleased():
        #     self.solenoid.set(DoubleSolenoid.Value.kForward)
        #     time.sleep(0.5)
        #     self.solenoid.set(DoubleSolenoid.Value.kReverse)
            # self.solenoidp1.toggle()
            # self.solenoidp2.toggle()



        # angle = self.drive_controller.getRightX()
        # speed = self.drive_controller.getLeftY()
        # if (abs(angle) > 0.001 or abs(speed) > 0.001):
        #     self.drive.arcadeDrive(-angle * SPEED_MULTIPLIER, speed * SPEED_MULTIPLIER, True)
        # else:
        #     self.drive.arcadeDrive(0, 0, True)


        # shooter
        # if self.drive_controller.getLeftTriggerAxis() > 0.01:
        #     self.shooter_motor_master.set(-(self.drive_controller.getLeftTriggerAxis()))
        #     self.shooter_motor_slave.set(-self.drive_controller.getLeftTriggerAxis())
        #     print("Shooter speed: " + str(self.drive_controller.getLeftTriggerAxis()))
        # elif self.drive_controller.getRightTriggerAxis() > 0.01:
        #     self.shooter_motor_master.set(self.drive_controller.getRightTriggerAxis())
        #     self.shooter_motor_slave.set(self.drive_controller.getRightTriggerAxis())
        #     # print("Shooter speed: " + str(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT)))
        # else:
        #     self.shooter_motor_master.set(0)
        #     self.shooter_motor_slave.set(0)


        # intake
        if self.drive_controller.getLeftBumper():
            self.intake_motor.set(0.4)
            self.sd.putValue("Intake: ", "Counter-Clockwise")
        elif self.drive_controller.getRightBumper():
            self.intake_motor.set(-0.4)
            self.sd.putValue("Intake: ", "Clockwise")
        else:
            self.intake_motor.set(0)
            self.sd.putValue("Intake: ", "Not Spinning")


        # tower
        if self.drive_controller.getAButton():
            self.tower_motor.set(0.3)
            self.sd.putValue("Tower: ", "Going Up")
        elif self.drive_controller.getBButton():
            self.tower_motor.set(-0.3)
            self.sd.putValue("Tower: ", "Going Down")
        else:
            self.tower_motor.set(0)
            self.sd.putValue("Tower: ", "Not Spinning")



        # if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
        #     self.shifter_shiftsolenoid.set(False)
        # if self.drive_controller.getStickButtonReleased(CONTROLLER_RIGHT):
        #     self.shifter_shiftsolenoid.set(True)




        #--------- Update SmartDashboard with motor speeds ---------#
        # self.sd.putNumber('Left Master Speed: ', self.drivetrain_left_motor_master.get())
        # self.sd.putNumber("Left Slave Speed: ", self.drivetrain_left_motor_slave.get())
        # self.sd.putNumber('Right Master Speed: ', self.drivetrain_right_motor_master.get())
        # self.sd.putNumber("Right Slave Speed: ", self.drivetrain_right_motor_slave.get())


if __name__ == '__main__':
    wpilib.run(SpartaBot)