"""
Software driver for a stepper motor. code originally inspired by ...
https://github.com/christophrumpel/test_stepper
https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/
"""
import abc
from time import sleep
from logging import getLogger

from linearstage import coils

_LOGGER = getLogger("motor")


class DriveScheme(abc.ABC):
    """
    https://en.wikipedia.org/wiki/Stepper_motor#/media/File:Drive.png
    """
    @abc.abstractproperty
    def name(self):
        return

    @abc.abstractproperty
    def sequence(self):
        return


class FullStepDriveScheme(DriveScheme):
    name = "Full Step"
    sequence = [
        coils.State(1, 0, 0, 1),
        coils.State(1, 0, 0, 1),
        coils.State(1, 1, 0, 0),
        coils.State(1, 1, 0, 0),
        coils.State(0, 1, 1, 0),
        coils.State(0, 1, 1, 0),
        coils.State(0, 0, 1, 1),
        coils.State(0, 0, 1, 1),
    ]


class WaveDriveScheme(DriveScheme):
    name = "Wave"
    sequence = [
        coils.State(1, 0, 0, 0),
        coils.State(1, 0, 0, 0),
        coils.State(0, 1, 0, 0),
        coils.State(0, 1, 0, 0),
        coils.State(0, 0, 1, 0),
        coils.State(0, 0, 1, 0),
        coils.State(0, 0, 0, 1),
        coils.State(0, 0, 0, 1),
    ]


class HalfStepDriveScheme(DriveScheme):
    name = "Half Step"
    sequence = [
        coils.State(1, 0, 0, 1),
        coils.State(1, 0, 0, 0),
        coils.State(1, 1, 0, 0),
        coils.State(0, 1, 0, 0),
        coils.State(0, 1, 1, 0),
        coils.State(0, 0, 1, 0),
        coils.State(0, 0, 1, 1),
        coils.State(0, 0, 0, 1),
    ]


class UnipolarStepperMotor:
    _MS_DELAY = 20
    """
    Drives a unipolar stepper motor

    Args:
        coils (linearstage.coil.Coils): An object that defines the motor's
            physical coils.
        drive_scheme (linearstage.motor.DriveScheme): The drive scheme for the
            coils in the motor that provides the sequence of states to be
            passed to the coils when a step is requested.
        ms_delay (int): The delay between setting states of the coils in the
            motor to allow the rotor to move in response to changing excitation.

    Attributes:
        ms_delay (int): ms delay between steps in the drive sequence
        drive_scheme (str): name of the motor drive scheme
    """
    def __init__(
            self,
            coils: coils.Coils,
            drive_scheme=FullStepDriveScheme,
            ms_delay=None):
        self._coils = coils
        self._delay = ms_delay if ms_delay is not None else self._MS_DELAY
        self._drive_scheme = drive_scheme
        _LOGGER.info(
            "Instantiated with coils: %r, delay: %d, drive_scheme: %s",
            coils, self._delay, self._drive_scheme.name)

    @property
    def drive_scheme(self) -> str:
        """
        The motor's drive scheme

        Returns:
            (str): The motor's drive scheme
        """
        return self._drive_scheme.name

    @property
    def ms_delay(self):
        """
        Delay between setting states on the motor's coils

        Returns:
            (int): The delay in ms
        """
        return self._delay

    def deactivate(self):
        """
        Deactivate all coils in the stepper motor. This may be useful to save
        running current through the motor when not in use.
        """
        _LOGGER.debug("Deactivating coils")
        self._coils.deactivate()

    def forward(self, cycles: int):
        """
        Step the motor forward the given number of complete cycles

        Args:
            cycles (int): the number of complete cycles to move
        """
        _LOGGER.debug("Moving forward %r steps", cycles)
        for _ in range(cycles):
            self._rotate_forward()
        _LOGGER.debug("Done")

    def backward(self, cycles: int):
        """
        Rotate the motor backward the given number of complete cycles

        Args:
            cycles (int): the number of complete cycles to move
        """
        _LOGGER.debug("Moving backward %r steps", cycles)
        for _ in range(cycles):
            self._rotate_backward()
        _LOGGER.debug("Done")

    def _set_step(self, step):
        self._coils.set_state(step)

    def _rotate_forward(self):
        for step in self._drive_scheme.sequence:
            self._set_step(step)
            sleep(self._delay / 1000)

    def _rotate_backward(self):
        for step in reversed(self._drive_scheme.sequence):
            self._set_step(step)
            sleep(self._delay / 1000)
