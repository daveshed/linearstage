#pylint: disable=missing-docstring
#pylint: enable=missing-docstring
import logging

from stage.endstop import EndStop
from stage.factory.base import StageFactoryBase
from stage.factory.config import Configurator
from stage.gpio import mock as mockgpio
from stage.motor.mock import MockMotor

_LOGGER = logging.getLogger("MOCK")


class FakeTrackHardware:
    #pylint: disable=too-few-public-methods
    """
    A simulation of the stage hardware. This holds the actual position of the
    stage and rules that govern its movement:
    1) end stop is triggered when the stage reaches its limit
    2) end stop is not triggered when the stage is within bounds
    3) movement is bounded to limits and any movement outside of these limits
       will raise an exception

    Args:
        end_stop: An end stop instance that will be driven by the
            FakeTrackHardware - It will be triggered when the stage reaches the
            end of its travel.
    """
    def __init__(self, end_stop):
        self._position = 0
        self._end_stop = end_stop

    @property
    def position(self):
        """
        The current position of the stage
        """
        return self._position

    @position.setter
    def position(self, request: int):
        if request > MockStageFactory.MAX_STAGE_LIMIT:
            raise AssertionError("Oh no. The motor has come off the track!")
        if request <= MockStageFactory.MIN_STAGE_LIMIT:
            self._end_stop.input.activate()
            self._position = 0
        else:
            self._end_stop.input.deactivate()
            self._position = request
        _LOGGER.info("position is %d", request)


class MockStageFactory(StageFactoryBase):
    """
    A factory that injects a mock end stop and mock motor into the stage for
    tests

    Args:
        config (Configurator): config object that contains necessary parameters
    """
    MIN_STAGE_LIMIT = 0
    MAX_STAGE_LIMIT = 100

    def __init__(self, config: Configurator):
        super().__init__()
        self._config = config
        self._end_stop = self._create_end_stop()
        self._fake_track = FakeTrackHardware(self._end_stop)
        self._motor = self._create_motor()

    @property
    def maximum_position(self):
        return type(self).MAX_STAGE_LIMIT

    @property
    def minimum_position(self):
        return type(self).MIN_STAGE_LIMIT

    @property
    def end_stop(self):
        return self._end_stop

    @property
    def motor(self):
        return self._motor

    def _create_motor(self):
        return MockMotor(self._fake_track)

    def _create_end_stop(self):
        return EndStop(
            mockgpio.InputChannel(
                self._config.end_stop_pin,
                self._config.end_stop_active_low))
