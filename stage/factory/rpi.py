#pylint: disable=missing-docstring
#pylint: enable=missing-docstring
from stage.endstop import EndStop
from stage.factory.base import StageFactoryBase
from stage.factory.config import Configurator
from stage.gpio import rpi
from stage.motor.coil import Coils
from stage.motor.stepper import UnipolarStepperMotor


class RPiMonopolarStepperStageFactory(StageFactoryBase):
    """
    A factory that creates motor and end stop required to instantiate a stage

    Args:
        config (Configurator): config object that holds all specific parameters
            needed to configure the stage factory
    """
    _DIGITAL_INPUT = rpi.InputChannel
    _DIGITAL_OUTPUT = rpi.OutputChannel

    def __init__(self, config: Configurator):
        self._config = config
        self._motor = self._create_motor()
        self._end_stop = self._create_end_stop()

    @property
    def maximum_position(self):
        return self._config.maximum_position

    @property
    def minimum_position(self):
        return self._config.minimum_position

    @property
    def motor(self):
        return self._motor

    @property
    def end_stop(self):
        return self._end_stop

    def _create_end_stop(self):
        return EndStop(
            type(self)._DIGITAL_INPUT(
                self._config.end_stop_pin,
                self._config.end_stop_active_low))

    def _create_motor(self):
        coils = Coils(
            *(type(self)._DIGITAL_OUTPUT(pin)
              for pin in self._config.motor_pins))
        return UnipolarStepperMotor(coils)
