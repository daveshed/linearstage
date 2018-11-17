import unittest
from unittest.mock import Mock, patch, call

#################### patch gpio module before import ###########################
import sys
mock_gpio = Mock()
mock_time = Mock()
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = mock_gpio
sys.modules['time'] = mock_time
################################################################################
from linearstage.config import (
    COIL_A1_PIN,
    COIL_A2_PIN,
    COIL_B1_PIN,
    COIL_B2_PIN,
    SEQUENCE,
    setup_logger,
)
from linearstage.motor import Motor

SINGLE_STEP_FORWARD = [
    call(13, 0),
    call(26, 1),
    call(6, 0),
    call(19, 0),
    call(13, 0),
    call(26, 1),
    call(6, 0),
    call(19, 1),
    call(13, 0),
    call(26, 0),
    call(6, 0),
    call(19, 1),
    call(13, 1),
    call(26, 0),
    call(6, 0),
    call(19, 1),
    call(13, 1),
    call(26, 0),
    call(6, 0),
    call(19, 0),
    call(13, 1),
    call(26, 0),
    call(6, 1),
    call(19, 0),
    call(13, 0),
    call(26, 0),
    call(6, 1),
    call(19, 0),
    call(13, 0),
    call(26, 1),
    call(6, 1),
    call(19, 0)
]

SINGLE_STEP_BACKWARD = [
    call(13, 0),
    call(26, 1),
    call(6, 1),
    call(19, 0),
    call(13, 0),
    call(26, 0),
    call(6, 1),
    call(19, 0),
    call(13, 1),
    call(26, 0),
    call(6, 1),
    call(19, 0),
    call(13, 1),
    call(26, 0),
    call(6, 0),
    call(19, 0),
    call(13, 1),
    call(26, 0),
    call(6, 0),
    call(19, 1),
    call(13, 0),
    call(26, 0),
    call(6, 0),
    call(19, 1),
    call(13, 0),
    call(26, 1),
    call(6, 0),
    call(19, 1),
    call(13, 0),
    call(26, 1),
    call(6, 0),
    call(19, 0)
]

class StepperMotorTestGroup(unittest.TestCase):
    
    def setUp(self):
        mock_gpio.reset_mock()
        self.motor = Motor([
            COIL_A1_PIN,
            COIL_A2_PIN,
            COIL_B1_PIN,
            COIL_B2_PIN
        ], SEQUENCE)

    def test_forward_step_gpio_sequence(self):
        self.motor.forward(steps=1)
        mock_gpio.output.assert_has_calls(SINGLE_STEP_FORWARD)

    def test_backward_gpio_sequence(self):
        self.motor.backward(steps=3)
        mock_gpio.output.assert_has_calls(SINGLE_STEP_BACKWARD)
        mock_gpio.output.assert_has_calls(SINGLE_STEP_BACKWARD)
        mock_gpio.output.assert_has_calls(SINGLE_STEP_BACKWARD)

    def test_deactivate_turns_off_coils(self):
        self.motor.deactivate()
        mock_gpio.output.assert_has_calls(
            calls=[call(13, 0), call(26, 0), call(6, 0), call(19, 0),],
            any_order=True)
