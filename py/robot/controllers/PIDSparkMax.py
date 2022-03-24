from rev import CANSparkMax, ControlType, MotorType
from rev._rev import


class PIDSparkMax:
    """
    Wrapper for a Rev Spark MAX that exposes all the
    PID setup and makes it easy to set a PID setpoint.
    """

    kP = 0.035  # 6e-2
    kI = 0.01  # 1e-3
    kD = 0.001  # 0.2
    kIz = 0.001
    kFF = 0.000015
    kMinOutput = -1
    kMaxOutput = 1
    control_mode = ControlType.kVelocity

    def __init__(self, canid):
        self.motor = CANSparkMax(canid, MotorType.kBrushless)
        self.motor.restoreFactoryDefaults()
        self.motor.setClosedLoopRampRate(1)
        self._motor_pid = self.motor.getPIDController()
        self._motor_pid.setP(self.kP)
        self._motor_pid.setI(self.kI)
        self._motor_pid.setD(self.kD)
        self._motor_pid.setIZone(self.kIz)
        self._motor_pid.setFF(self.kFF)
        self._motor_pid.setOutputRange(self.kMinOutput, self.kMaxOutput)
        self.motor.setSmartCurrentLimit(10)

    def setP(self, value):
        self.kP = value
        self._motor_pid.setP(value)

    def setI(self, value):
        self.kI = value
        self._motor_pid.setI(value)

    def setD(self, value):
        self.kD = value
        self._motor_pid.setD(value)

    def setIz(self, value):
        self.kIz = value
        self._motor_pid.setIZone(value)

    def setFF(self, value):
        self.kFF = value
        self._motor_pid.setFF(value)

    def setMOutputRange(self, min, max):
        self.kMinOutput = min
        self.kMaxOutput = max
        self._motor_pid.setOutputRange(value)

    def getEncoder(self):
        return self.motor.getEncoder()

    def stop(self):
        self.motor.stopMotor()

    def set(self, setpoint):
        self._motor_pid.setReference(setpoint, self.control_mode)

    def setPID(self, kP, kI, kD):
        self.setP(kP)
        self.setI(kI)
        self.setD(kD)

    def fromKu(self, Ku: float, Tu: float) -> None:
        """
        Use the Zeigler-Nichols method to tune the PID based off the oscillations.
        Uses a P value for oscillation along with the period of the oscullations to find the PID values.
        Args:
            Ku: This is the value of P that you obtain by increasing P slowly until the system starts to oscillate
            Tu: This is the period of the oscillation, with one full stroke
        """
        self.setP(0.6 * Ku)
        self.setI(1.2 * Ku / Tu)
        self.setD(3 * Ku * Tu / 40)

    @property
    def rpm(self):
        return self.motor.getEncoder().getVelocity()