import logging
import unittest
from unittest import mock

from stage import exceptions
from stage.stage import Stage
from stage import endstop
from stage.gpio import mock as mockgpio
from stage.factory.mock import FakeTrackHardware, MockStageFactory
from stage.factory.config import Configurator



class TrackTests(unittest.TestCase):
    ENDSTOP_PIN_IDX = 4
    MAXIMUM_IDX = MockStageFactory.MAX_STAGE_LIMIT
    MINIMUM_IDX = MockStageFactory.MIN_STAGE_LIMIT

    def position_from_percent(self, percent):
        # calculate the position as a percentage of allowed travel
        return (self.stage.max - self.stage.min) \
            * (percent / 100) + self.stage.min

    def setUp(self):
        config = Configurator(
            maximum_position=self.MAXIMUM_IDX,
            minimum_position=self.MINIMUM_IDX,
            motor_pins=None,
            end_stop_pin=None,
            end_stop_active_low=True)
        self.factory = MockStageFactory(config)
        self.stage = Stage(self.factory)
        self.mock_end_stop = self.factory.end_stop

    def test_position_limits_configured(self):
        self.assertEqual(self.stage.max, self.MAXIMUM_IDX)
        self.assertEqual(self.stage.min, self.MINIMUM_IDX)

    def test_home_resets_position(self):
        self.stage.position = self.position_from_percent(50)
        self.stage.home()
        self.assertEqual(self.stage.min, self.stage.position)
        self.assertTrue(self.mock_end_stop.triggered)

    def test_end_moves_stage_to_max_position(self):
        self.stage.end()
        self.assertFalse(self.mock_end_stop.triggered)
        self.assertEqual(self.stage.position, self.stage.max)

    def test_position_within_bounds_updates_position_ok(self):
        target_position = self.position_from_percent(10)
        self.stage.position = target_position
        self.assertEqual(target_position, self.stage.position)
        self.assertFalse(self.mock_end_stop.triggered)

    def test_request_out_of_range_raises_assert(self):
        target_position = self.stage.max + 1
        with self.assertRaises(exceptions.OutOfRangeError):
            self.stage.position = target_position
        target_position = self.stage.min - 1
        with self.assertRaises(exceptions.OutOfRangeError):
            self.stage.position = target_position
