import logging
import unittest
from unittest import mock

from stage import error
from stage.stage import Stage, StageBuilder
from stage.gpio import GpioBase

LOGGER = logging.getLogger("MOCKS")
MIN_STAGE_LIMIT = 0
MAX_STAGE_LIMIT = 100


class MockEndStop:

    def __init__(self):
        self._triggered = False
        self._callbacks = []

    @property
    def triggered(self):
        return self._triggered

    def trigger(self):
        # for tests only...
        self._triggered = True
        for callback in self._callbacks:
            callback()

    def reset(self):
        # for tests only...
        self._triggered = False

    def register_callback(self, callback):
        self._callbacks.append(callback)

    def deregister_callback(self, callback):
        self._callbacks.remove(callback)


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
    def __init__(self, end_stop):
        self._position = 0
        self._end_stop = end_stop

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, request: int):
        if request > MAX_STAGE_LIMIT:
            raise AssertionError("Oh no. The motor has come off the track!")
        if request <= MIN_STAGE_LIMIT:
            self._end_stop.trigger()
            self._position = 0
        else:
            self._end_stop.reset()
            self._position = request
        LOGGER.info("position is %d", request)


class TrackTests(unittest.TestCase):

    def setUp(self):
        self.mock_end_stop = MockEndStop()
        self.mock_motor = MockMotor(FakeStageHardware(self.mock_end_stop))
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


class BuilderTestGroup(unittest.TestCase):

    def test_stage_builder_can_instantiate(self):
        # MockGpio.triggered = True
        end_stop_pin = 22
        def fake_input_triggered(pin):
            nonlocal end_stop_pin
            if pin == end_stop_pin:
                return True
            raise Exception("%d not configured" % pin)
        mock_gpio = mock.Mock(
            spec=GpioBase, input_triggered=fake_input_triggered)
        stage = (
            StageBuilder()
                .build_gpio(interface=mock_gpio)
                .build_coils(
                    a1_pin=26,
                    b1_pin=19,
                    a2_pin=13,
                    b2_pin=6)
                .build_motor(drive_scheme='Half Step', ms_delay=10)
                .build_end_stop(pin=22, active_low=True)
                .build_track(
                    min_limit=MIN_STAGE_LIMIT, max_limit=MAX_STAGE_LIMIT)
                .build_linear_stage()
                .get_stage())
        self.assertEqual(stage.max, MAX_STAGE_LIMIT)
        # TODO: Other asserts eg stage.min
