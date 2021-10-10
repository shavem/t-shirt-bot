import wpilib
import magicbot
from ctre import WPI_TalonFX

class ShooterTest:

    shooter_motor = WPI_TalonFX

    # This is changed to the value in robot.py
    shootspeed = 0.0

    # This gets reset after each invocation of execute()
    shootEnable = False

    def on_enable(self):
        """Called when the robot enters teleop or autonomous mode
        self.logger.info(
            "Robot is enabled: I have SOME_CONSTANT=%s", self.SOME_CONSTANT
        )
        """

    def do_something(self, speed):
        self.shootspeed = speed
        self.shootEnable = True

    def execute(self):
        if self.shootEnable:
            self.shooter_motor.set(self.shootspeed)
        shootEnable = False