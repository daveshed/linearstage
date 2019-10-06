import logging

from stage.endstop import EndStop
from stage.factory.base import StageFactoryBase
from stage.gpio import mock as mockgpio
from stage.motor.mock import MockMotor

_LOGGER = logging.getLogger("MOCK")


class FakeTrackHardware:
    """
    A simulation of the stage hardware. This holds the actual position of the
    stage and rules that govern its movement:
    1) end stop is triggered when the stage reaches its limit
    2) end stop is not triggered when the stage is within bounds
    3) movement is bounded to limits and any movement outside of these limits
       will raise an exception
    """
    def __init__(self, end_stop):
        self._position = 0
        self._end_stop = end_stop

    @property
    def position(self):
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
    MIN_STAGE_LIMIT = 0
    MAX_STAGE_LIMIT = 100

    def __init__(self, config):
        super().__init__()
        self._end_stop = self._create_end_stop(config)
        self._fake_track = FakeTrackHardware(self._end_stop)
        self._motor = self._create_motor()

    def _create_motor(self):
        return MockMotor(self._fake_track)

    @staticmethod
    def _create_end_stop(config):
        return EndStop(
            mockgpio.InputChannel(
                config.end_stop_pin,
                config.end_stop_active_low))

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
