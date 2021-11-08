import math


def scale(input, input_min, input_max, output_min, output_max):
    """
    Scales an input from one range to another

    :param input: The input on the input range
    :param input_min: The minimum of the input range
    :param input_max: The maximum of the input range
    :param output_min: The minimum of the output range
    :param output_max: The maximum of the output range

    :return: The input value scaled to the output range.
    """
    return ((input - input_min) / (input_max - input_min) *
            (output_max - output_min)) + output_min


def clamp(input, mininum, maximum):
    """
    Clamps an input within a range

    :param input: The input
    :param mininum: The minimum of the output range
    :param maximum: The maximum of the output range

    :return: The input value clamped to the output range.
    """
    return max(min(input, maximum), mininum)


def abs_clamp(input, abs_minimum, abs_maximum):
    """
    Clamps an input within a absolute value range

    :param input: The input
    :param mininum: The minimum of the output range
    :param maximum: The maximum of the output range

    :return: The input value clamped to the abs output range.
    """
    return math.copysign(clamp(abs(input), abs_minimum, abs_maximum), input)
