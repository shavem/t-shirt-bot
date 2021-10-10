from ctre import WPI_TalonSRX
from magicbot import tunable
from constants import TALON_TIMEOUT
from wpilib import PIDController
from enum import IntEnum

class WristPosition(IntEnum):
    START = 50
    PLACE = 2100

class Wrist:

    motor = WPI_TalonSRX

    kP = tunable(0.3)
    kI = tunable(0.0)
    kD = tunable(0.0)
    kF = tunable(0.15)

    setpoint = tunable(0)
    value = tunable(0)
    error = tunable(0)

    def setup(self):

        self.motor.setSensorPhase(True)
        self.motor.setInverted(False)
        self.motor.configSelectedFeedbackSensor(
            WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative, 0, 0)
        
        self.motor.setStatusFramePeriod(
            WPI_TalonSRX.StatusFrameEnhanced.Status_13_Base_PIDF0, 10, TALON_TIMEOUT
        )
        self.motor.setStatusFramePeriod(
            WPI_TalonSRX.StatusFrameEnhanced.Status_10_MotionMagic, 10, TALON_TIMEOUT
        )
        
        self.motor.configNominalOutputForward(0, TALON_TIMEOUT)
        self.motor.configNominalOutputReverse(0, TALON_TIMEOUT)
        self.motor.configPeakOutputForward(.25, TALON_TIMEOUT)
        self.motor.configPeakOutputReverse(-.25, TALON_TIMEOUT)

        self.motor.selectProfileSlot(0, 0)
        self.motor.config_kP(0, self.kP, 0)
        self.motor.config_kI(0, self.kI, 0)
        self.motor.config_kD(0, self.kD, 0)
        self.motor.config_kF(0, self.kF, 0)

        self.motor.configMotionCruiseVelocity(1500, TALON_TIMEOUT)
        self.motor.configMotionAcceleration(600, TALON_TIMEOUT)
        self.motor.setSelectedSensorPosition(0, 0, TALON_TIMEOUT)

    def move_to(self, position):
        self.setpoint = position

    def raise_to_placement(self):
        self.move_to(WristPosition.PLACE)

    def return_to_start(self):
        self.move_to(WristPosition.START)

    def is_encoder_connected(self):
        return self.motor.getPulseWidthRiseToRiseUs() != 0

    def get_position(self):
        return self.motor.getSelectedSensorPosition(0)
    
    def reset_position(self):
        self.motor.setSelectedSensorPosition(0, 0, TALON_TIMEOUT)
        self.setpoint = 0

    def stop(self):
        self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        self.setpoint = 0

    def execute(self):        
        # For debugging
        #print('wrist',
        #      'setpoint', self.setpoint,
        #      'val', self.value,
        #      'err', self.error,
        #      'curr_pos', self.motor.getQuadraturePosition(),
        #      'curr_velo', self.motor.getQuadratureVelocity())

        self.motor.set(WPI_TalonSRX.ControlMode.MotionMagic, self.setpoint)

        try:
            self.value = self.motor.getSelectedSensorPosition(0)
            self.error = self.motor.getClosedLoopError(0)
        except NotImplementedError:
            # Simulator doesn't implement getError
            pass            

    def on_disable(self):
        self.stop()