

class Configurator:
    """
    Configures the various options needed to make a linearstage. It is used
    by concrete stage factories to retreive information about the setup.
    """
    def __init__(self, motor_pins, end_stop_pin, end_stop_active_low):
        self._motor_pins = motor_pins
        self._end_stop_pin = end_stop_pin
        self._end_stop_active_low = end_stop_active_low

    @property
    def motor_pins(self):
        return self._motor_pins

    @property
    def end_stop_pin(self):
        return self._end_stop_pin

    @property
    def end_stop_active_low(self):
        return self._end_stop_active_low
