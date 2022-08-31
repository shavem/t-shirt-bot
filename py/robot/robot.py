import wpilib
import rev
import magicbot
from magicbot import state, timed_state
import wpilib.drive
from networktables import NetworkTables
import logging
import ctre
from robotpy_ext.autonomous import AutonomousModeSelector
# from limelight import limelight
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
ANGLE_MULTIPLIER = 0.7

magicbot.MagicRobot.control_loop_wait_time = 0.02


# class ShooterAutomation(magicbot.StateMachine):
#     # Some other component
#     shooter: Shooter
#
#     def fire(self, speed):
#         """This is called from the main loop."""
#         self.speed = speed
#         self.engage()
#
#     @state(first=True)
#     def begin_firing(self):
#         """
#         This function will only be called IFF fire is called and
#         the FSM isn't currently in the 'firing' state. If fire
#         was not called, this function will not execute.
#         """
#         self.shooter.shoot(self.speed)
#         if self.shooter.is_ready:
#             self.next_state('firing')
#
#     @timed_state(duration=1.0, must_finish=True)
#     def firing(self):
#         """
#         Because must_finish=True, once the FSM has reached this state,
#         this state will continue executing even if engage isn't called.
#         """
#         self.shooter.shoot(self.speed)
#         # self.ball_pusher.push()


class SpartaBot(magicbot.MagicRobot):
    # shooter_automation: ShooterAutomation

    # shooter: Shooter



    def disabledPeriodic(self):
        # self.shooter.limelight_state = 1
        # self.shooter.limelight.light(1)
        self.sd.putValue("Mode", "Disabled")
        # NetworkTables.getTable("limelight").putNumber("ledMode", 1)
        # limelight.LEDState(1)


    def createObjects(self):
        wpilib.CameraServer.launch()


        # Initialize SmartDashboard
        logging.basicConfig(level=logging.DEBUG)
        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd = NetworkTables.getTable('SmartDashboard')

        self.limelight = NetworkTables.getTable("limelight")

        # self.compressor = wpilib.Compressor(PNEUMATICS_MODULE_TYPE)
        # self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 2, 3)
        # # self.solenoid.set(DoubleSolenoid.Value.kReverse)
        # self.sd.putValue("Gear", "Unchanged")

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
        # self.drive.setExpiration(0.01)

        # ---Shooter--- #
        #
        # Left
        self.shooter_motor_left = ctre.WPI_TalonFX(10)
        # Right
        self.shooter_motor_right = ctre.WPI_TalonFX(9)

        # ---Intake--- #
        self.intake_motor = rev.CANSparkMax(1, MOTOR_BRUSHED)
        self.tower_motor = rev.CANSparkMax(2, MOTOR_BRUSHED)

        # wpilib.CameraServer.launch()
        self.automodes = AutonomousModeSelector("autonomous")

    # def autonomousInit(self):
    #     # self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
    #     # self.intake_arm_solenoid.set(DoubleSolenoid.Value.kReverse)
    #     print("auton started")
    #     self.automodes.start()

    # def autonomous(self):
    #     self.automodes.periodic()
    #     # self.drive.arcadeDrive(0, 0, True)
    #
    #     # @timed_state(first=True, duration=2, next_state="shoot")
    #     # def test():
    #     #     print("aiming")
    #     #     self.drive.arcadeDrive(0, 0, True)
    #     #     # self.shooter.limelight_state = 3
    #     #     # limelight_data = self.shooter.aim()
    #     #     # self.drivetrain.vision_aim(*limelight_data)
    #     #
    #     # @timed_state(duration=8, next_state="reverse")
    #     # def shoot():
    #     #     self.drive.arcadeDrive(0, 0, True)
    #     #     print("shooting")
    #     #     # self.shooter.shoot()
    #     #
    #     # @timed_state(duration=2, next_state="stop")
    #     # def reverse():
    #     #     print("reversing")
    #     #     # self.shooter.limelight_state = 1
    #     #     # # self.intake_sm.engage()
    #     #     # self.drivetrain.arcadeDrive(-0.5, 0, 0)
    #     #
    #     # @state
    #     # def stop():
    #     #     print("stopping")
    #     #     # self.drivetrain.arcadeDrive(0, 0, 0)
    #
    # def disabledInit(self):
    #     self.automodes.disable()

    def teleopInit(self):
        self.sd.putValue("Mode", "Teleop")
        # Set shooter falcons to coast mode
        # self.shooter_motor_left.setNeutralMode(ctre.NeutralMode(1))
        # self.shooter_motor_left.setNeutralMode(ctre.NeutralMode(1))
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
        if (abs(angle) > 0.03 or abs(speed) > 0.03):
            self.drive.arcadeDrive(-angle * ANGLE_MULTIPLIER, -speed * SPEED_MULTIPLIER, True)
            # self.sd.putValue('Drivetrain: ', -speed)
            self.sd.putValue("Speed ", speed)
            self.sd.putValue("Angle ", angle)
        else:
            self.drive.arcadeDrive(0, 0, True)
            self.sd.putValue("Drivetrain: ", "Stopped")

        # shooter
        if self.drive_controller.getLeftTriggerAxis() > 0.05:
            # self.shooter_motor_left.set(self.drive_controller.getLeftTriggerAxis())
            # self.shooter_motor_right.set(-self.drive_controller.getLeftTriggerAxis())
            # self.sd.putValue("Shooter: ", -self.drive_controller.getLeftTriggerAxis())
            self.intake_motor.set(-0.5)
        elif self.drive_controller.getBButton():
            self.intake_motor.set(0.3)
            self.sd.putValue("Intake: ", "Out")
        else:
            self.intake_motor.set(0)


            # self.shooter_automation.fire(-self.drive_controller.getLeftTriggerAxis())
            # print("Shooter speed: " + str(self.drive_controller.getLeftTriggerAxis()))

        if self.drive_controller.getAButton():
            self.shooter_motor_left.set(-0.5)
            self.shooter_motor_right.set(0.5)
            self.sd.putValue("Shooter: ", 0.5)
        elif self.drive_controller.getRightTriggerAxis() > 0.05:
            self.shooter_motor_left.set(-self.drive_controller.getRightTriggerAxis())
            self.shooter_motor_right.set(self.drive_controller.getRightTriggerAxis())
            self.sd.putValue("Shooter: ", self.drive_controller.getRightTriggerAxis())
            # self.shooter_automation.fire(self.drive_controller.getRightTriggerAxis())
            # print("Shooter speed: " + str(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT)))
        else:
            self.shooter_motor_left.set(0)
            self.shooter_motor_right.set(0)
            self.sd.putValue("Shooter: ", 0)

        # intake
        # if self.drive_controller.getBButton():
        #     self.intake_motor.set(0.3)
        #     self.sd.putValue("Intake: ", "Out")
        # elif self.drive_controller.getAButton():
        #     self.intake_motor.set(-0.5)
        #     self.sd.putValue("Intake: ", "In")
        # else:
        #     self.intake_motor.set(0)
        #     self.sd.putValue("Intake: ", "0")

        # tower
        if self.drive_controller.getRightBumper():
            self.tower_motor.set(0.7)
            self.sd.putValue("Tower: ", "Down")
        elif self.drive_controller.getLeftBumper():
            self.tower_motor.set(-0.7)
            self.sd.putValue("Tower: ", "Up")
        else:
            self.tower_motor.set(0)
            self.sd.putValue("Tower: ", "0")


        # aimbot
        if self.drive_controller.getYButton():
            try:
                self.turn = self.limelight.getNumber('tx', None) / 30.75
                print(self.turn)
                self.drive.arcadeDrive(self.turn, 0)
            except Exception:
                print("didn't work")

        self.sd.putValue("Targets", self.limelight.getNumber('tv', None))
        self.sd.putValue("Horizontal offset", self.limelight.getNumber('tx', None))
        self.sd.putValue("Vertical offset", self.limelight.getNumber('ty', None))



        # if self.drive_controller.getLeftStickButtonReleased():
        #     self.solenoid.set(DoubleSolenoid.Value.kForward)
        #     self.sd.putValue("Gear", "Low")
        # if self.drive_controller.getRightStickButtonReleased():
        #     self.solenoid.set(DoubleSolenoid.Value.kReverse)
        #     self.sd.putValue("Gear", "High")




        # if self.drive_controller.getXButtonReleased():
        #     self.solenoid.toggle()


        # if self.drive_controller.getXButtonReleased():
        #     self.solenoid.toggle()
        #     print(self.solenoid.get())
        #     self.sd.putValue("Gear", self.solenoid.get())

        # --------- Update SmartDashboard with motor speeds ---------#
        # self.sd.putNumber('Left Master Speed: ', self.drivetrain_left_motor_master.get())
        # self.sd.putNumber("Left Slave Speed: ", self.drivetrain_left_motor_slave.get())
        # self.sd.putNumber('Right Master Speed: ', self.drivetrain_right_motor_master.get())
        # self.sd.putNumber("Right Slave Speed: ", self.drivetrain_right_motor_slave.get())


if __name__ == '__main__':
    wpilib.run(SpartaBot)

