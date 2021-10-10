import wpilib


def rumble(joystick, level):
    joystick.setRumble(
        wpilib.XboxController.RumbleType.kLeftRumble, level)
    joystick.setRumble(
        wpilib.XboxController.RumbleType.kRightRumble, level)
