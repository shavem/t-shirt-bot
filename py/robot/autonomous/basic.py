from magicbot import AutonomousStateMachine, tunable, timed_state
import networktables
from wpilib.drive import DifferentialDrive
from rev import CANSparkMax
from ctre import WPI_TalonFX
import time


# from components.component2 import Component2


class basic(AutonomousStateMachine):
    MODE_NAME = "basic"
    DEFAULT = True

    # component2: Component2
    sd: networktables.NetworkTable
    drive: DifferentialDrive
    intake_motor: CANSparkMax
    tower_motor: CANSparkMax
    shooter_motor_left: WPI_TalonFX
    shooter_motor_right: WPI_TalonFX

    # drive_speed = tunable(-1)

    @timed_state(duration=1.5, next_state="pickup_ball", first=True)
    def taxi(self):
        self.sd.putValue("Mode", "Pickup ball")
        self.drive.arcadeDrive(0, -0.4, True)

    @timed_state(duration=1.5, next_state="go_back")
    def pickup_ball(self):
        self.drive.arcadeDrive(0, -0.4, True)
        self.intake_motor.set(-0.5)
        self.sd.putValue("Mode", "pickup")

    @timed_state(duration=0.5, next_state="spin_shooter")
    def go_back(self):
        self.drive.arcadeDrive(0, 0.4, True)

    @timed_state(duration=3, next_state="shoot")
    def spin_shooter(self):
        self.shooter_motor_left.set(-0.8)
        self.shooter_motor_right.set(0.8)

    @timed_state(duration=3, next_state="stop")
    def shoot(self):
        self.tower_motor.set(-0.3)

    @timed_state(duration=10.5)
    def stop(self):
        self.shooter_motor_left.set(0)
        self.shooter_motor_right.set(0)
        self.tower_motor.set(0)
        self.intake_motor.set(0)
        self.drive.arcadeDrive(0, 0, True)

        # self.component2.do_something()
