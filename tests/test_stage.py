import logging
import unittest
from unittest import mock

from stage import error
from stage.stage import Stage
from stage import endstop
from stage.gpio import mock as mockgpio

LOGGER = logging.getLogger("MOCKS")
MIN_STAGE_LIMIT = 0
MAX_STAGE_LIMIT = 100


class MockMotor:

    def __init__(self, stage):
        self.deactivated = False
        self._stage = stage

    def forward(self, steps: int):
        LOGGER.info("Mock motor forward %d steps", steps)
        self._stage.position += steps

    def backward(self, steps: int):
        LOGGER.info("Mock motor backward %d steps", steps)
        self._stage.position -= steps

    def deactivate(self):
        self.deactivated = True


class FakeStageHardware:
    """
    A simulation of the stage hardware. This holds the actual position of the
    stage and rules that govern its movement:
    1) end stop is triggered when the stage reaches its limit
    2) end stop is not triggered when the stage is within bounds
    3) movement is bounded to limits and any movement outside of these limits
       will raise an exception
    """
    def __init__(self, end_stop_input):
        self._position = 0
        self._input = end_stop_input

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, request: int):
        if request > MAX_STAGE_LIMIT:
            raise AssertionError("Oh no. The motor has come off the track!")
        if request <= MIN_STAGE_LIMIT:
            self._input.activate()
            self._position = 0
        else:
            self._input.deactivate()
            self._position = request
        LOGGER.info("position is %d", request)


class TrackTests(unittest.TestCase):
    ENDSTOP_PIN_IDX = 4

    def create_mock_endstop(self):
        return end_stop_inst

    def setUp(self):
        self.input_inst = mockgpio.InputChannel(
            pin=self.ENDSTOP_PIN_IDX, active_low=True, gpio=None)
        self.mock_end_stop = endstop.EndStop(self.input_inst)
        self.mock_motor = MockMotor(
            FakeStageHardware(end_stop_input=self.input_inst))
        self.stage = Stage(
            motor=self.mock_motor,
            end_stop=self.mock_end_stop,
            min_limit=MIN_STAGE_LIMIT,
            max_limit=MAX_STAGE_LIMIT,
        )

    def test_home_resets_position(self):
        self.assertEqual(MIN_STAGE_LIMIT, self.stage.position)
        self.assertTrue(self.mock_end_stop.triggered)

    def test_end_moves_stage_to_max_position(self):
        self.stage.end()
        self.assertEqual(MAX_STAGE_LIMIT - MIN_STAGE_LIMIT, self.stage.position)
        self.assertFalse(self.mock_end_stop.triggered)
        self.assertEqual(self.stage.position, self.stage.max)

    def test_position_within_bounds_updates_position_ok(self):
        target_position = 10
        self.stage.position = target_position
        self.assertEqual(target_position, self.stage.position)
        self.assertFalse(self.mock_end_stop.triggered)

    def test_request_out_of_range_raises_assert(self):
        target_position = MAX_STAGE_LIMIT + 1
        with self.assertRaises(error.OutOfRangeError):
            self.stage.position = target_position
        target_position = MIN_STAGE_LIMIT - 1
        with self.assertRaises(error.OutOfRangeError):
            self.stage.position = target_position
