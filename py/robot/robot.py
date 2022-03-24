import wpilib
import rev
import magicbot
from magicbot import state, timed_state
import wpilib.drive
from networktables import NetworkTables
import logging
import ctre
from components.shooter import Shooter
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

# CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
# CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand
PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed
SPEED_MULTIPLIER = 1

magicbot.MagicRobot.control_loop_wait_time = 0.02


class ShooterAutomation(magicbot.StateMachine):
    # Some other component
    shooter: Shooter

    def fire(self):
        """This is called from the main loop."""
        self.engage()

    @state(first=True)
    def begin_firing(self):
        """
        This function will only be called IFF fire is called and
        the FSM isn't currently in the 'firing' state. If fire
        was not called, this function will not execute.
        """
        self.shooter.shoot()
        if self.shooter.is_ready():
            self.next_state('firing')

    @timed_state(duration=1.0, must_finish=True)
    def firing(self):
        """
        Because must_finish=True, once the FSM has reached this state,
        this state will continue executing even if engage isn't called.
        """
        self.shooter.shoot()
        # self.ball_pusher.push()





class SpartaBot(magicbot.MagicRobot):
    shooter_automation: ShooterAutomation

    shooter: Shooter

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
        self.drivetrain_right_motor_master = ctre.WPI_TalonFX(6)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonFX(7)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonFX(8)
        self.drivetrain_left_motor_master = ctre.WPI_TalonFX(3)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonFX(4)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonFX(5)
        self.left = wpilib.SpeedControllerGroup(
            self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave, self.drivetrain_left_motor_slave2)
        self.right = wpilib.SpeedControllerGroup(
            self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave, self.drivetrain_right_motor_slave2)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        # wpilib.drive.DifferentialDrive.setExpiration(0.01)
        self.drive.setExpiration(1)

        # ---Shooter--- #
        #
        # Left
        # self.shooter_motor_left = ctre.WPI_TalonFX(10)
        # Right
        # self.shooter_motor_right = ctre.WPI_TalonFX(9)

        # ---Intake--- #
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

        angle = self.drive_controller.getRightX()
        speed = self.drive_controller.getLeftY()
        if (abs(angle) > 0.01 or abs(speed) > 0.01):
            self.drive.arcadeDrive(-angle * SPEED_MULTIPLIER, speed * SPEED_MULTIPLIER, True)
            self.sd.putValue('Drivetrain: ', -speed)
        else:
            self.drive.arcadeDrive(0, 0, True)
            self.sd.putValue("Drivetrain: ", "Stopped")

        # shooter
        if self.drive_controller.getLeftTriggerAxis() > 0.01:
            # self.shooter_motor_left.set(-self.drive_controller.getLeftTriggerAxis())
            # self.shooter_motor_right.set(self.drive_controller.getLeftTriggerAxis())
            self.sd.putValue("Shooter: ", -self.drive_controller.getLeftTriggerAxis())
            # self.shooter_automation.fire()
            # print("Shooter speed: " + str(self.drive_controller.getLeftTriggerAxis()))
        elif self.drive_controller.getRightTriggerAxis() > 0.01:
            # self.shooter_motor_left.set(self.drive_controller.getRightTriggerAxis())
            # self.shooter_motor_right.set(-self.drive_controller.getRightTriggerAxis())
            self.sd.putValue("Shooter: ", self.drive_controller.getRightTriggerAxis())
            # self.shooter_automation.fire()
            # print("Shooter speed: " + str(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT)))
        else:
            # self.shooter_motor_left.set(0)
            # self.shooter_motor_right.set(0)
            self.sd.putValue("Shooter: ", 0)


        # intake
        if self.drive_controller.getLeftBumper():
            self.intake_motor.set(0.4)
            self.sd.putValue("Intake: ", "Out")
        elif self.drive_controller.getRightBumper():
            self.intake_motor.set(-0.4)
            self.sd.putValue("Intake: ", "In")
        else:
            self.intake_motor.set(0)
            self.sd.putValue("Intake: ", "0")

        # tower
        if self.drive_controller.getAButton():
            self.tower_motor.set(0.5)
            self.sd.putValue("Tower: ", "Down")
        elif self.drive_controller.getBButton():
            self.tower_motor.set(-0.5)
            self.sd.putValue("Tower: ", "Up")
        else:
            self.tower_motor.set(0)
            self.sd.putValue("Tower: ", "0")

        # if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
        #     self.shifter_shiftsolenoid.set(False)
        # if self.drive_controller.getStickButtonReleased(CONTROLLER_RIGHT):
        #     self.shifter_shiftsolenoid.set(True)

        # --------- Update SmartDashboard with motor speeds ---------#
        # self.sd.putNumber('Left Master Speed: ', self.drivetrain_left_motor_master.get())
        # self.sd.putNumber("Left Slave Speed: ", self.drivetrain_left_motor_slave.get())
        # self.sd.putNumber('Right Master Speed: ', self.drivetrain_right_motor_master.get())
        # self.sd.putNumber("Right Slave Speed: ", self.drivetrain_right_motor_slave.get())


if __name__ == '__main__':
    wpilib.run(SpartaBot)
