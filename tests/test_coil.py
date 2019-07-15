import unittest
from unittest import mock

#################### patch gpio module before import ###########################
import sys
mock_gpio = mock.Mock(OUT='OUTPUT')
sys.modules['RPi.GPIO'] = mock_gpio
################################################################################
#...now import code under test...
from linearstage import coil
from linearstage import coils


class CoilTestGroup(unittest.TestCase):

    def setUp(self):
        self.expected_pin = 10
        self.expected_label = "a1"
        self.coil = coil.Coil(self.expected_label, self.expected_pin)

    def test_coil_instantiation_activates_output_and_deactivates(self):
        self.assertEqual(self.coil.label, self.expected_label)
        mock_gpio.assert_has_calls([
            mock.call.setup(self.expected_pin, 'OUTPUT'),
            mock.call.output(self.expected_pin, 0)])
        self.assertFalse(self.coil.active)

    def test_coil_on_switches_on_output(self):
        mock_gpio.reset_mock()
        self.coil.on()
        mock_gpio.assert_has_calls([mock.call.output(self.expected_pin, 1)])
        self.assertTrue(self.coil.active)

    def test_coil_off_switches_off_output(self):
        mock_gpio.reset_mock()
        self.coil.off()
        mock_gpio.assert_has_calls([mock.call.output(self.expected_pin, 0)])
        self.assertFalse(self.coil.active)


class StateSettingTestGroup(unittest.TestCase):

    def test_set_state_sets_correct_coils(self):
        state = coils.State(1, 0, 0, 1)
        a1 = coil.Coil("a1", 1)
        b1 = coil.Coil("b1", 2)
        a2 = coil.Coil("a2", 3)
        b2 = coil.Coil("b2", 4)
        foo = coils.Coils(a1, b1, a2, b2)
        foo.set_state(state)
        self.assertTrue(a1.active)
        self.assertFalse(b1.active)
        self.assertFalse(a2.active)
        self.assertTrue(b2.active)
