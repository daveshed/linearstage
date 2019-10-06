import unittest
from unittest import mock

from stage.gpio import error
#################### patch gpio module before import ###########################
import sys
MOCK_GPIO = mock.Mock()
# This only seems to work in python 3.7
sys.modules['RPi.GPIO'] = MOCK_GPIO
################################################################################
from stage.gpio import rpi


class GpioOutputTestGroup(unittest.TestCase):

    def setUp(self):
        MOCK_GPIO.reset_mock()
        self.pin_idx = 1
        self.output = rpi.OutputChannel(pin=self.pin_idx)

    def test_initialising_output_calls_setup_set_low(self):
        MOCK_GPIO.setup.assert_called_with(
            self.pin_idx, MOCK_GPIO.OUT)
        self.assertEqual(self.output.pin, self.pin_idx)
        MOCK_GPIO.output.assert_called_with(self.pin_idx, 0)
        self.assertFalse(self.output.state)

    def test_set_high_calls_ouput(self):
        self.output.activate()
        MOCK_GPIO.output.assert_called_with(self.pin_idx, 1)
        self.assertTrue(self.output.state)

    def test_set_low_calls_output(self):
        self.output.deactivate()
        MOCK_GPIO.output.assert_called_with(self.pin_idx, 0)
        self.assertFalse(self.output.state)


class FakeEventCaptureMixin:

    class EventConfiguration:

        def __init__(self, channel, edge, callback, bouncetime):
            self._channel = channel
            self._edge = edge
            self._callback = callback
            self._bouncetime = bouncetime

        @property
        def channel(self):
            return self._channel

        @property
        def edge(self):
            return self._edge

        @property
        def callback(self):
            return self._callback

        @property
        def bouncetime(self):
            return self._bouncetime

    def fake_add_event_detect(self, channel, edge, callback, bouncetime):
        self.event_config = \
            self.EventConfiguration(channel, edge, callback, bouncetime)

    def fake_rising_event(self):
        if self.event_config.edge == "RISING":
            self.event_config.callback(self.event_config.channel)

    def fake_falling_event(self):
        if self.event_config.edge == "FALLING":
            self.event_config.callback(self.event_config.channel)

    def setup_mock_gpio(self):
        MOCK_GPIO.reset_mock(side_effect=True)
        MOCK_GPIO.add_event_detect.side_effect = self.fake_add_event_detect
        MOCK_GPIO.FALLING = "FALLING"
        MOCK_GPIO.RISING = "RISING"


class GpioInputActiveLowTestGroup(unittest.TestCase, FakeEventCaptureMixin):

    def setUp(self):
        self.setup_mock_gpio()
        self.event_config = None
        self.pin_idx = 1
        self.active_low = True
        self.input = rpi.InputChannel(
            pin=self.pin_idx, active_low=self.active_low)

    def test_initialising_input_calls_setup(self):
        MOCK_GPIO.setup.assert_called_with(
            self.pin_idx, MOCK_GPIO.IN, MOCK_GPIO.PUD_UP)
        self.assertEqual(
            self.event_config.bouncetime, rpi.InputChannel._DEBOUNCE_MS)
        self.assertEqual(
            self.event_config.edge, 'FALLING')

    def test_retreiving_state_reads_gpio_high_signal_returns_false(self):
        MOCK_GPIO.input.return_value = 1
        self.assertFalse(self.input.state)
        MOCK_GPIO.input.assert_called()

    def test_retreiving_state_reads_gpio_low_signal_returns_true(self):
        MOCK_GPIO.input.return_value = 0
        self.assertTrue(self.input.state)
        MOCK_GPIO.input.assert_called()

    def test_input_activated_invokes_callbacks(self):
        foo = mock.Mock()
        bar = mock.Mock()
        self.input.register_callback(foo)
        self.input.register_callback(bar)
        # input is active low so a falling edge should invoke callbacks
        self.fake_falling_event()
        foo.assert_called()
        bar.assert_called()


class GpioInputActiveHighTestGroup(unittest.TestCase, FakeEventCaptureMixin):

    def setUp(self):
        self.setup_mock_gpio()
        self.pin_idx = 1
        self.active_low = False
        self.input = rpi.InputChannel(
            pin=self.pin_idx, active_low=self.active_low)

    def test_initialising_input_calls_setup(self):
        MOCK_GPIO.setup.assert_called_with(
            self.pin_idx, MOCK_GPIO.IN, MOCK_GPIO.PUD_DOWN)
        self.assertEqual(
            self.event_config.edge, 'RISING')

    def test_retreiving_state_reads_gpio_high_signal_returns_true(self):
        MOCK_GPIO.input.return_value = 1
        self.assertTrue(self.input.state)
        MOCK_GPIO.input.assert_called()

    def test_retreiving_state_reads_gpio_low_signal_returns_false(self):
        MOCK_GPIO.input.return_value = 0
        self.assertFalse(self.input.state)
        MOCK_GPIO.input.assert_called()

    def test_input_activated_invokes_callbacks(self):
        foo = mock.Mock()
        bar = mock.Mock()
        self.input.register_callback(foo)
        self.input.register_callback(bar)
        # input is active high so a rising edge should invoke callbacks
        self.fake_rising_event()
        foo.assert_called()
        bar.assert_called()

    def test_input_activated_does_not_call_deregistered_callbacks(self):
        bar = mock.Mock()
        self.input.register_callback(bar)
        self.input.deregister_callback(bar)
        self.fake_rising_event()
        bar.assert_not_called()

    def test_cannot_deregister_callback_not_registered(self):
        bar = mock.Mock()
        with self.assertRaises(error.GpioError):
            self.input.deregister_callback(bar)

    def test_input_deactivated_does_not_invoke_callbacks(self):
        foo = mock.Mock()
        self.input.register_callback(foo)
        self.fake_falling_event()
        foo.assert_not_called()
