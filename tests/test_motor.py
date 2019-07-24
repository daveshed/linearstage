import unittest
from unittest import mock

from linearstage import motor


class StepperMotorAttributeTestGroup(unittest.TestCase):

    def setUp(self):
        self.fake_coils = mock.Mock(name='coils')
        self.motor = motor.UnipolarStepperMotor(
            coils=self.fake_coils,
            drive_scheme=motor.FullStepDriveScheme.name,
            ms_delay=0)

    def test_ms_delay_set_on_init_can_be_retreived(self):
        self.assertEqual(self.motor.ms_delay, 0)

    def test_drive_scheme_set_on_init_can_be_retreived(self):
        self.assertEqual(self.motor.drive_scheme, motor.FullStepDriveScheme.name)


class DriveSchemeTestMixin:
    drive_scheme = None

    def setUp(self):
        self.fake_coils = mock.Mock(name='coils')
        self.motor = motor.UnipolarStepperMotor(
            coils=self.fake_coils,
            drive_scheme=self.drive_scheme.name,
            ms_delay=0)

    def test_forward_step_gpio_sequence(self):
        self.motor.forward(cycles=1)
        self.fake_coils.set_state.assert_has_calls(
            [mock.call(state) for state in self.drive_scheme.sequence])

    def test_backward_gpio_sequence(self):
        self.motor.backward(cycles=3)
        expect = [mock.call(state) for state
            in reversed(self.drive_scheme.sequence)]
        self.fake_coils.set_state.assert_has_calls(expect)
        self.fake_coils.set_state.assert_has_calls(expect)
        self.fake_coils.set_state.assert_has_calls(expect)

    def test_deactivate_turns_off_coils(self):
        self.motor.deactivate()
        self.fake_coils.deactivate.assert_called()


class FullStepDriveSchemeTestGroup(DriveSchemeTestMixin, unittest.TestCase):
    drive_scheme = motor.FullStepDriveScheme


class WaveDriveSchemeTestGroup(DriveSchemeTestMixin, unittest.TestCase):
    drive_scheme = motor.WaveDriveScheme


class HalfStepDriveSchemeTestGroup(DriveSchemeTestMixin, unittest.TestCase):
    drive_scheme = motor.HalfStepDriveScheme
