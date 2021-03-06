import unittest
from unittest import mock

from stage.motor import stepper
from stage.motor import drive
from stage.motor import coil
from stage.gpio import mock as mockgpio


class StepperMotorAttributeTestGroup(unittest.TestCase):

    def setUp(self):
        self.fake_coils = mock.Mock(spec=coil.Coils)
        self.motor = stepper.UnipolarStepperMotor(
            coils=self.fake_coils,
            drive_scheme=drive.FullStepDriveScheme.name,
            ms_delay=0)

    def test_ms_delay_set_on_init_can_be_retreived(self):
        self.assertEqual(self.motor.ms_delay, 0)

    def test_drive_scheme_set_on_init_can_be_retreived(self):
        self.assertEqual(self.motor.drive_scheme, drive.FullStepDriveScheme.name)


class CoilActivationTestGroup(unittest.TestCase):
    FAKE_PINS = coil.Pins(1,2,3,4)

    def setUp(self):
        self.fake_coils = coil.Coils(
            *(mockgpio.OutputChannel(pin) for pin in type(self).FAKE_PINS))
        self.motor = stepper.UnipolarStepperMotor(
            coils=self.fake_coils,
            drive_scheme=drive.FullStepDriveScheme.name,
            ms_delay=0)

    def test_coils_deactivated_after_init(self):
        for coil in self.fake_coils.coils:
            self.assertFalse(coil.state)

    def test_correct_pins_initialised_as_outputs(self):
        for coil, pin in zip(self.fake_coils.coils, self.FAKE_PINS):
            self.assertEqual(coil.pin, pin)


class DriveSchemeTestMixin:
    drive_scheme = None

    def setUp(self):
        self.fake_coils = mock.Mock(spec=coil.Coils)
        self.motor = stepper.UnipolarStepperMotor(
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
            in reversed(self.drive_scheme.sequence)] * 3
        self.fake_coils.set_state.assert_has_calls(expect)

    def test_deactivate_turns_off_coils(self):
        self.motor.deactivate()
        self.fake_coils.deactivate.assert_called()


class FullStepDriveSchemeTestGroup(DriveSchemeTestMixin, unittest.TestCase):
    drive_scheme = drive.FullStepDriveScheme


class WaveDriveSchemeTestGroup(DriveSchemeTestMixin, unittest.TestCase):
    drive_scheme = drive.WaveDriveScheme


class HalfStepDriveSchemeTestGroup(DriveSchemeTestMixin, unittest.TestCase):
    drive_scheme = drive.HalfStepDriveScheme
