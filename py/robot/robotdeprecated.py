import wpilib
import ctre
import magicbot
import wpilib.drive
import wpilib.controller

from navx import AHRS
from enum import IntEnum
from common import rumbler
from components import drivetrain, intake, shooterFalcon, tower, feed #, climb, targeting
#from controllers import alignment_controller
#from networktables import NetworkTables

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand


class SpartaBot(magicbot.MagicRobot):

    drivetrain = drivetrain.Drivetrain
    intake = intake.Intake
    shooter = shooterFalcon.Shooter
    tower = tower.Tower
    feed = feed.Feed


    def createObjects(self):
        
        self.drive_controller = wpilib.XboxController(0)
        #self.compressor = wpilib.Compressor()

        #drivetrain
        
        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(1)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(2)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonSRX(3)

        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(4)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(5)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonSRX(6)

        '''
        self.drivetrain_left_motor_master = ctre.WPI_TalonFX(1)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonFX(2)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonFX(3)

        self.drivetrain_right_motor_master = ctre.WPI_TalonFX(4)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonFX(5)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonFX(6)


        self.left = wpilib.SpeedControllerGroup(
            self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave, self.drivetrain_left_motor_slave2
            )
        self.right = wpilib.SpeedControllerGroup(
            self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave, self.drivetrain_right_motor_slave2
        )
        self.spartaBot = DifferentialDrive(self.left, self.right)
        self.spartaBot.setExpiration(0.1)
        '''

        self.drive_shifter_solenoid = wpilib.Solenoid(1)
        #self.navx = navx.AHRS.create_spi()


        #intake
        self.intake_roller_motor = ctre.WPI_VictorSPX(12)
        self.intake_arm_solenoid = wpilib.DoubleSolenoid(2,3)

        #tower
        self.tower_motor = ctre.WPI_TalonSRX(8)

        #feed
        self.feed_motor_master = ctre.WPI_TalonSRX(7)
        self.feed_motor_slave = ctre.WPI_TalonSRX(9)

        #shooter
        #self.shooter_motor_master = ctre.WPI_VictorSPX(11)
        #self.shooter_motor_slave = ctre.WPI_VictorSPX(13)
        self.shooter_hood_solenoid = wpilib.DoubleSolenoid(4,5)
        self.shooter_motor = ctre.WPI_TalonFX(11)

        #climb
        self.climb_motor_master = ctre.WPI_TalonSRX(14)
        self.climb_motor_slave = ctre.WPI_TalonSRX(15)

        ''' limelight PID Turning
        self.PIDF = [2.5, 0.002, 10.0, 0.0]
        self.target_pos = self.tx
        self.pending_move = None
        self.target_angle = 0
        self.lock_target = False'''
        self.kP = 0
        self.kI = 0
        self.kD = 0



        #limelight
        #self.data = self.targeting.get_data()


    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #self.drivetrain.reset_angle_correction()
        pass



    def teleopPeriodic(self):
    #drivetrain
        
        angle = self.drive_controller.getX(CONTROLLER_RIGHT)
        self.drivetrain.angle_corrected_differential_drive(
            self.drive_controller.getY(CONTROLLER_LEFT), angle)
        if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
            self.drivetrain.shift_toggle()
            
        
        #self.spartaBot.tankDrive(self.drive_controller.getY(CONTROLLER_LEFT) * -1, self.drive_controller.getY(CONTROLLER_RIGHT) * -1)
        


    #intake
        if self.drive_controller.getBumper(CONTROLLER_RIGHT):
            self.intake.run_roller(1)
            #self.tower_feed_motor_master.set(0.3)
            #self.tower_feed_motor_slave.set(0.3)
            self.feed.run_feed(0.3)
        elif self.drive_controller.getAButton():
            self.intake.run_roller(-1)
            #self.tower_feed_motor_master.set(-0.4)
            #self.tower_feed_motor_slave.set(-0.4)
            self.feed.run_feed(-0.4)
        else:
            self.intake_roller_motor.stopMotor()
            #self.tower_feed_motor_master.set(0)
            #self.tower_feed_motor_slave.set(0)            
            self.feed_motor_master.stopMotor()
            self.feed_motor_slave.stopMotor()
            
        #intake arm deploy
        if self.drive_controller.getYButtonReleased():
            self.intake.switch()
        

    #tower
        '''
        self.tower_motor.set(-self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))

        if self.drive_controller.getYButtonReleased():
            self.tower.move_incremental(35000)
        elif self.drive_controller.getXButtonReleased():
            self.tower.move_incremental(-5000)
        '''

        if self.drive_controller.getTriggerAxis(CONTROLLER_LEFT)>0.2:
            self.tower_motor.set(-self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))
        elif self.drive_controller.getBumper(CONTROLLER_LEFT):
            self.tower_motor.set(0.5)
        else:
            self.tower_motor.set(0)
        
    #shooter
        if self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT)>0.8:
            self.shooter.run_shooter(0.95)
        elif self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT)>0.1:
            self.shooter.run_shooter(0.5)
        else:
            self.shooter_motor.stopMotor()
        
        #shooter angle change
        if self.drive_controller.getXButtonReleased():
            self.shooter.switch()
            
    #climb
        '''
        if self.drive_controller.getAButton():
            self.climb_motor_master.set(0.4)
            self.climb_motor_slave.set(0.4)
        elif self.drive_controller.getBButton():
            self.climb_motor_master.set(-0.4)
            self.climb_motor_slave.set(-0.4)
        elif self.drive_controller.getYButton():
            self.climb_motor_master.set(-0.4)
        elif self.drive_controller.getXButton():
            self.climb_motor_slave.set(-0.4)
        else:
            self.climb_motor_master.stopMotor()
            self.climb_motor_slave.stopMotor()       
        ''' 


if __name__ == '__main__':
    wpilib.run(SpartaBot)
