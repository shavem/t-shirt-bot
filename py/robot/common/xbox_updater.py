from networktables import NetworkTables


def push(joystick, name):
    table = NetworkTables.getTable('robot')
    output_dictionary = {
        name + '/AButton': joystick.getAButton(),
        name + '/BButton': joystick.getBButton(),
        name + '/BackButton': joystick.getBackButton(),
        name + '/StartButton': joystick.getStartButton(),
        name + '/XButton': joystick.getXButton(),
        name + '/YButton': joystick.getYButton(),
        name + '/LeftRumble': joystick.leftRumble,
        name + '/RightRumble': joystick.rightRumble,
        name + '/LeftX': joystick.getX(joystick.Hand.kLeft),
        name + '/LeftY': joystick.getY(joystick.Hand.kLeft),
        name + '/RightX': joystick.getX(joystick.Hand.kRight),
        name + '/RightY': joystick.getY(joystick.Hand.kRight),
        name + '/LeftTrigger': joystick.getTriggerAxis(joystick.Hand.kLeft),
        name + '/RightTrigger': joystick.getTriggerAxis(joystick.Hand.kRight),
        name + '/LeftBumper': joystick.getBumper(joystick.Hand.kLeft),
        name + '/RightBumper': joystick.getBumper(joystick.Hand.kRight)
    }

    for i in output_dictionary.keys():
        table.putValue(i, output_dictionary[i])
