# from limelight import limelight

from magicbot import will_reset_to, tunable, feedback
# from controllers.PIDSparkMax import PIDSparkMax
import networktables


import wpilib
from ctre import TalonSRX, ControlMode


from typing import Tuple


class Shooter:
    limelight_state = will_reset_to(1)
    motor_rpm = will_reset_to(0)
    feeder_motor_speed = will_reset_to(0)

    target_rpm = tunable(0.5)
    feed_speed_setpoint = tunable(-1)
    rpm_error = tunable(300)
    x_aim_error = tunable(1.2)
    y_aim_error = tunable(2)

    # motor: PIDSparkMax
    shooter_motor_left: TalonSRX
    shooter_motor_right: TalonSRX
    intake_motor: TalonSRX
    sd: networktables.NetworkTable

    # camera_state: int

    # @property
    # def target_rpm(self):
    #     _, y = self.aim()
    #     return -1 * (5.232 * pow(y, 2) - 70.76 * y + 3300)

    def setup(self):
        """
        Runs right after the createObjects method is run.
        Sets up all the networktables values and configures
        the shooter motor PID values
        """
        # self.limelight = limelight.Limelight()

        self.log()

        # Shooter motor configuration
        # self.motor.fromKu(0.0008, 0.6)  # P = 0.03, I = 0.05, D = 0.125
        # self.motor.setFF(1 / 5880)
        # self.motor.setFF(0)
        # self.motor.setPID(.0008, 0, 0)
        # self.motor.setPID(0.0015, 0.008, 0.005)
        # self.motor._motor_pid.setIZone(0.5)
        # self.motor.motor.setSmartCurrentLimit(100)

    # @feedback
    # def aim(self) -> Tuple[float, float]:
    #     """
    #     Will return the distances from the crosshair
    #     """
    #     # self.limelight_state = 3
    #     # self.camera_state = 0
    #     x = self.limelight.horizontal_offset
    #     y = self.limelight.vertical_offset
    #     return (x, y)

    # @property
    # def is_aimed(self):
    #     """
    #     Test whether the target is within a tolerance
    #     """
    #     x, y = self.aim()
    #     if abs(x) > self.x_aim_error:
    #         return False
    #     # if abs(y) > self.y_aim_error:
    #     #     return False
    #     return True

    @property
    def is_ready(self):
        """
        Returns whether the current rpm of the motor is within
        a certain range, specified by the `rpm_error` property
        """
        return (
            self.rpm_error + self.motor_rpm
            > ((self.shooter_motor_right.get() + self.shooter_motor_left.get()) / 2)
            > -self.rpm_error + self.motor_rpm
        )

    def shoot(self):
        """
        Sets the shooter to start moving toward the setpoint
        """
        self.motor_rpm = self.target_rpm

    def feed(self):
        """
        Start the feeder to move the power cells towards the flywheel
        """
        self.feeder_motor_speed = self.feed_speed_setpoint

    def backdrive(self):
        """
        Start the feeder to move the power cells towards the flywheel
        """
        self.feeder_motor_speed = 1

    def execute(self):
        # self.limelight.light(self.limelight_state)
        # self.limelight.pipeline(self.limelight_state)
        if abs(self.motor_rpm) < 0.02:
            self.shooter_motor_right.stopMotor()
            self.shooter_motor_left.stopMotor()
        else:
            self.shooter_motor_right.set(self.motor_rpm)
            self.shooter_motor_left.set(self.motor_rpm)
        if (
            abs(self.motor_rpm) > 0.05
            and abs((self.shooter_motor_left.get() + self.shooter_motor_right.get()) / 2) > abs(self.motor_rpm) - self.rpm_error
        ) or self.feeder_motor_speed:
            if not self.feeder_motor_speed:
                self.feed()
            self.intake_motor.set(ControlMode.PercentOutput, self.feeder_motor_speed)
        else:
            self.intake_motor.set(ControlMode.PercentOutput, 0)
        # self.feeder_motor.set(ControlMode.PercentOutput, self.feeder_motor_speed)
        self.log()

    def log(self):
        """
        Get values relating to the shooter and post them
        to the dashboard for logging reasons.
        """
        # wpilib.SmartDashboard.putBoolean(
        #     "limelightLightState", True if self.limelight_state == 3 else False
        # )
        self.sd.putBoolean("shooterReady", self.is_ready)
        # wpilib.SmartDashboard.putBoolean("isAimed", self.is_aimed)
        # wpilib.SmartDashboard.putBoolean("targetsFound", self.limelight.valid_targets)
        self.sd.putNumber("shooterSpeedTarget", abs(self.motor_rpm))
        self.sd.putNumber("shooterMotorSpeed", abs((self.shooter_motor_right.get() + self.shooter_motor_left.get()) / 2))
        self.sd.putNumber("shooterOutput", (self.shooter_motor_right.getOutputCurrent() + self.shooter_motor_left.getOutputCurrent()) / 2)