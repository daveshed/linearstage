import unittest
from unittest import mock

from linearstage import coil
from linearstage import gpio


class CoilTestGroup(unittest.TestCase):

    def setUp(self):
        self.expected_pin = 10
        self.expected_label = "a1"
        self.mock_gpio = mock.Mock(name='gpio', spec=gpio.base.GpioBase)
        self.coil = coil.Coil(
            self.expected_label, self.expected_pin, self.mock_gpio)

    def test_coil_instantiation_activates_output_and_deactivates(self):
        self.assertEqual(self.coil.label, self.expected_label)
        self.mock_gpio.assert_has_calls([
            mock.call.initialise_output(self.expected_pin),
            mock.call.set_low(self.expected_pin)])
        self.assertFalse(self.coil.active)

    def test_coil_on_switches_on_output(self):
        self.mock_gpio.reset_mock()
        self.coil.on()
        self.mock_gpio.assert_has_calls([mock.call.set_high(self.expected_pin)])
        self.assertTrue(self.coil.active)

    def test_coil_off_switches_off_output(self):
        self.mock_gpio.reset_mock()
        self.coil.off()
        self.mock_gpio.assert_has_calls([mock.call.set_low(self.expected_pin)])
        self.assertFalse(self.coil.active)


class StateSettingTestGroup(unittest.TestCase):

    def test_set_state_sets_correct_coils(self):
        state = coil.State(1, 0, 0, 1)
        a1 = coil.Coil("a1", 1, mock.Mock())
        b1 = coil.Coil("b1", 2, mock.Mock())
        a2 = coil.Coil("a2", 3, mock.Mock())
        b2 = coil.Coil("b2", 4, mock.Mock())
        foo = coil.Coils(a1, b1, a2, b2)
        foo.set_state(state)
        self.assertTrue(a1.active)
        self.assertFalse(b1.active)
        self.assertFalse(a2.active)
        self.assertTrue(b2.active)
