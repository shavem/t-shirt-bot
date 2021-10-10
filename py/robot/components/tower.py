import math
from magicbot import tunable
from ctre import WPI_TalonSRX
from enum import IntEnum
from wpilib import DoubleSolenoid, DigitalInput
from constants import TALON_TIMEOUT

class EncoderPositions(IntEnum):
    POSITION1 = 100
    POSITION2 = 750
    POSITION3 = 1500
    POSITION4 = 2250
    POSITION5 = 3000
    POSITION6 = 3750

class Tower:
    USE_MOTIONMAGIC = True

    motor = WPI_TalonSRX
    
    kFreeSpeed = tunable(0.3)
    kZeroingSpeed = tunable(0.1)
    kP = tunable(0.3)
    kI = tunable(0.0)
    kD = tunable(0.0)
    kF = tunable(0.0)

    kCruiseVelocity = 30000
    kAcceleration = 24000

    setpoint = tunable(0)
    value = tunable(0)
    error = tunable(0)

    def setup(self):
        self.pending_position = None
        self.pending_drive = None
        self._temp_hold = None

        self.has_zeroed = False
        self.needs_brake = False
        self.braking_direction = None

        self.buffer = [ EncoderPositions.POSITION1,
                    EncoderPositions.POSITION2,
                    EncoderPositions.POSITION3,
                    EncoderPositions.POSITION4,
                    EncoderPositions.POSITION5,
                    EncoderPositions.POSITION6
                        ]
            
        self.index = 0

        self.motor.setInverted(False)
        self.motor.configSelectedFeedbackSensor(
            WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative, 0, 0)
        self.motor.selectProfileSlot(0, 0)
        self.motor.setSensorPhase(True)


        self.motor.config_kP(0, self.kP, 0)
        self.motor.config_kI(0, self.kI, 0)
        self.motor.config_kD(0, self.kD, 0)
        self.motor.config_kF(0, self.kF, 0)

        self.motor.configPeakOutputReverse(-0.3, TALON_TIMEOUT)

        try:
            self.motor.configMotionCruiseVelocity(self.kCruiseVelocity, 0)
            self.motor.configMotionAcceleration(self.kAcceleration, 0)
        except NotImplementedError:
            # Simulator - no motion profiling support
            self.USE_MOTIONMAGIC = False

    def is_encoder_connected(self):
        return self.motor.getPulseWidthRiseToRiseUs() != 0

    def get_encoder_position(self):
        return self.motor.getSelectedSensorPosition(0)

    def is_at_lowest(self):
        return self.get_encoder_position() <= LOWEST_POSITION

    def is_at_position(self, position):
        return abs(self.get_encoder_position() - position) <= \
            POSITION_TOLERANCE

    def make_lowest_position(self):
        self.pending_position = EncoderPositions.POSITION1

    def toggle(self, pos=True):
        if self.index+1 < 6:
            self.index+=1
            self.pending_position = self.buffer[self.index]
        else:
            self.index = 0
            self.pending_position = self.buffer[self.index]
        print(self.pending_position)
        #elif not pos and self.index-1 in range(len(self.buffer)):
        #    self.index-=1

    def move_to(self, amount):
        '''
        Move `amount` inches.
        '''
        self.pending_position = amount

    def raise_freely(self):
        self.pending_drive = self.kFreeSpeed

    def lower_freely(self):
        self.pending_drive = -self.kFreeSpeed

    def move_incremental(self,x):
        self.move_to(self.setpoint+x)

    def execute(self):
        # For debugging
        #print('elevator', 'drive', self.pending_drive, 'lim', self.reverse_limit.get(),
        #      'pending_pos', self.pending_position,
        #      'setpoint', self.setpoint,
        #      'val', self.value,
        #      'err', self.error,
        #      'curr_pos', self.motor.getQuadraturePosition(),
        #      'curr_velo', self.motor.getQuadratureVelocity())

        # Brake - apply the brake either when we reach peak of movement
        # (for upwards motion), and thus ds/dt = v = 0, or else immediately
        # if we're traveling downwards (since no e.z. way to sense gravity vs
        # intertial movement).
        if self.needs_brake:
            if self.pending_drive:
                self.needs_brake = False
            else:
                velocity = self.motor.getQuadratureVelocity()
                if velocity == 0 or \
                        self.braking_direction == -1 or \
                        velocity / abs(velocity) != self.braking_direction:
                    self.pending_position = self.motor.getQuadraturePosition()
                    self.needs_brake = False
                    self.braking_direction = None

        # Elevator motor
        if self.pending_drive:
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput,
                           self.pending_drive)
            self.pending_drive = None
            self.pending_position = None  # Clear old pending position
            self._temp_hold = None

        elif self.pending_position is not None and self.is_encoder_connected():
            # Note: we don't clear the pending position so that we keep
            # on driving to the position in subsequent execute() cycles.

            # If not zeroed, try out "best shot" at getting to desired places
            '''if not self.has_zeroed:
                if self.pending_position == ElevatorPosition.GROUND or \
                        self.pending_position == ElevatorPosition.ROCKET1:
                    # Drive downwards until we zero it
                    self._temp_hold = None
                    self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput,
                                   -self.kZeroingSpeed)
                else:
                    # Hopefully it's at the start of the match and we're still
                    # near the top. Just hold position right where we are
                    if not self._temp_hold:
                        self._temp_hold = self.motor.getQuadraturePosition()
                    self.motor.set(WPI_TalonSRX.ControlMode.MotionMagic,
                                   self._temp_hold)'''

            # Otherwise, if we're zeroed, just set position normally
            if self.has_zeroed:
                self._temp_hold = None
                if self.USE_MOTIONMAGIC:
                    self.motor.set(WPI_TalonSRX.ControlMode.MotionMagic,
                                   self.pending_position)
                else:
                    self.motor.set(WPI_TalonSRX.ControlMode.Position,
                                   self.pending_position)

        else:
            if self.is_encoder_connected():
                # If no command, hold position in place (basically, a more
                # "aggressive" brake mode to prevent any slippage).
                self.needs_brake = True
                velocity = self.motor.getQuadratureVelocity()
                self.braking_direction = velocity / abs(velocity or 1)
            self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)

        # Update dashboard PID values
        if self.pending_position:
            try:
                self.setpoint = self.motor.getClosedLoopTarget(0)
                self.value = self.motor.getSelectedSensorPosition(0)
                self.error = self.motor.getClosedLoopError(0)
            except NotImplementedError:
                # Simulator doesn't implement getError
                pass

    def get_state(self):
        return {
            'pending_position': self.pending_position
        }

    def put_state(self, state):
        self.pending_position = state['pending_position']