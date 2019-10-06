from stage import exceptions
from stage.factory.base import StageFactoryBase


class RPiMonopolarStepperStageFactory(StageFactoryBase):
    _DIGITAL_INPUT = rpi.InputChannel
    _DIGITAL_OUTPUT = rpi.OutputChannel

    def __init__(self, config):
        self._motor = self._create_motor(config)

    @staticmethod
    def _create_motor(config):
        coils = Coils(*(type(self)_DIGITAL_OUTPUT(pin) for pin in config.motor_pins))
        return UnipolarStepperMotor(coils)

    def set_motor_pins(self, a1, b1, a2, b2):
        self._motor_pins = Pins(a1, b1, a2, b2)

    def get_motor(self):
        return self._motor

    def get_end_stop(self):
        return EndStop(
            type(self)._DIGITAL_INPUT(
                cls.get_end_stop_pin(),
                cls.get_end_stop_active_low()))
