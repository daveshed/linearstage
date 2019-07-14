import logging
import unittest
from unittest import mock

from linearstage import error
from linearstage.stage import Stage

logger = logging.getLogger("mocks")


MIN_STAGE_LIMIT = 0
MAX_STAGE_LIMIT = 100

class MockEndStop:

    def __init__(self):
        self._triggered = False

    @property
    def triggered(self):
        return self._triggered

    @triggered.setter
    def triggered(self, state):
        self._triggered = state
        logger.info("end stop set to {}".format(state))


class MockMotor:

    def __init__(self, observer):
        self.deactivated = False
        self._observer = observer

    def forward(self, steps):
        logger.info("Mock motor forward {} steps".format(steps))
        self._observer.position += steps

    def backward(self, steps):
        logger.info("Mock motor backward {} steps".format(steps))
        self._observer.position -= steps

    def deactivate(self):
        self.deactivated = True


class FakeTrackHardware:
    """
    A simulation of the stage hardware. This holds the actual position of the
    stage and rules that govern its movement:
    1) end stop is triggered when the stage reaches its limit
    2) end stop is not triggered when the stage is within bounds
    3) movement is bounded to limits and any movement outside of these limits
       will raise an exception
    """
    def __init__(self, end_stop, position=0):
        self._position = position
        self._end_stop = end_stop

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, request):
        if request >= MIN_STAGE_LIMIT:
            self._end_stop.triggered = True
        self._position = request
        logger.info("position is {}".format(request))


class TrackTests(unittest.TestCase):

    def setUp(self):
        self.mock_end_stop = MockEndStop()
        self.mock_motor = MockMotor(
            observer=FakeTrackHardware(
                end_stop=self.mock_end_stop,
                position=23))
        self.stage = Stage(
            self.mock_motor,
            self.mock_end_stop,
            MIN_STAGE_LIMIT,
            MAX_STAGE_LIMIT
        )

    def test_home_resets_position(self):
        self.assertEqual(0, self.stage.position)

    def test_end_moves_stage_to_max_position(self):
        self.stage.end()
        self.assertEqual(MAX_STAGE_LIMIT - MIN_STAGE_LIMIT, self.stage.position)

    def test_position_within_bounds_updates_position_ok(self):
        target_position = 10
        self.stage.position = target_position
        self.assertEqual(target_position, self.stage.position)

    def test_request_out_of_range_raises_assert(self):
        target_position = MAX_STAGE_LIMIT + 1
        with self.assertRaises(error.OutOfRangeError):
            self.stage.position = target_position
        target_position = MIN_STAGE_LIMIT - 1
        with self.assertRaises(error.OutOfRangeError):
            self.stage.position = target_position