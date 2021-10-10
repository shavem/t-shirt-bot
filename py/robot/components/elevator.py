import math
import magicbot
from magicbot import tunable
from ctre import WPI_TalonFX
from enum import IntEnum

UNITS_PER_REV = 4096
DISTANCE_PER_REV = math.pi * 1.786  # pi * sprocket diameter

class Elevator:

    USE_MOTIONMAGIC = True

    shooter_motor = WPI_TalonFX
    shooter_motor_slave =  WPI_TalonFX

    kFreeSpeed = tunable(0.1)
    kZeroingSpeed = tunable(0.1)
    kP = tunable(0.3)
    kI = tunable(0.0)
    kD = tunable(0.0)
    kF = tunable(0.0)

    kCruiseVelocity = 30000
    kAcceleration = 12000

    setpoint = tunable(0)
    value = tunable(0)
    error = tunable(0)
