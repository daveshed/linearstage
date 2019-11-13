#pylint: disable=missing-docstring
#pylint: enable=missing-docstring
from stage.exceptions import BadConfigurationData


class Configurator:
    """
    Configures the various options needed to make a linearstage. It is used
    by concrete stage factories to retreive information about the setup.

    TODO: Config should be loaded from a config file with specified path.
    Args:
        motor_pins (tuple): the required motor pins in order a1, b1, a2, b2
        maximum_position (int): the maximum position index
        minimum_position (int): the minimum position index
        motor_pins (tuple): the channels required to operate the stepper motor.
            Should be provided in the order in which they will be triggered eg.
            a1, b1, a2, b2.
        end_stop_pin (int): the input channel that the end_stop is connected to
        end_stop_active_low (int): True if the end stop is activated when its
            signal goes low
    """
    def __init__(self, **kwargs):
        try:
            self._maximum_position = kwargs['maximum_position']
            self._minimum_position = kwargs['minimum_position']
            self._motor_pins = kwargs['motor_pins']
            self._end_stop_pin = kwargs['end_stop_pin']
            self._end_stop_active_low = kwargs['end_stop_active_low']
        except KeyError as error:
            raise BadConfigurationData(
                "Failed to gather configuration data %r" % repr(error))

    @property
    def maximum_position(self):
        """The maximum position index of the stage"""
        return self._maximum_position

    @property
    def minimum_position(self):
        """The minimum position of the stage"""
        return self._minimum_position

    @property
    def motor_pins(self):
        """
        The output channels that the motor is connected to in sequence order
        """
        return self._motor_pins

    @property
    def end_stop_pin(self):
        """
        The input channel that the end stop is connected to"""
        return self._end_stop_pin

    @property
    def end_stop_active_low(self):
        """Whether or not the end stop is activated on a low signal"""
        return self._end_stop_active_low
