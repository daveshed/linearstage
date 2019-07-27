"""
Software driver for a stepper motor. code originally inspired by ...
https://github.com/christophrumpel/test_stepper
https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/
"""
from time import sleep
from logging import getLogger

from stage.coil import Coil


_LOGGER = getLogger("MOTOR")

class Motor:
    """
    A stepper motor driver.

    Keyword arguments:
    pins -- a list of pin numbers that the motor's coils are connected on
    sequence -- the sequence of pins to activate in order to step the motor
    ms_delay -- a time in ms to delay switching from one state to the next in
    the given sequence
    """
    def __init__(self, pins, sequence, ms_delay):
        _LOGGER.info("Instantiated on pins %r", pins)
        self._coils = [Coil(pin) for pin in pins]
        self._seq = sequence
        self._delay = ms_delay

    @classmethod
    def from_config(cls, config: dict):
        """
        Returns a a motor instance from a config dictionary

        Keyword arguments:
        config -- a config dictionary containing necessary configuration params
        """
        return cls(
            config['pins'],
            config['sequence'],
            config['ms_delay']
        )

    def deactivate(self):
        """
        Deactivate all coils in the stepper motor. This may be useful to save
        running current through the motor when not in use.
        """
        _LOGGER.info("Deactivating coils")
        for coil in self._coils:
            coil.off()

    def forward(self, steps: int):
        """
        Step the motor forward the given number of steps

        Keyword arguments:
        steps -- an integer number of steps to move
        """
        _LOGGER.debug("Moving forward %r steps", steps)
        for _ in range(steps):
            self._step_forward()
        _LOGGER.debug("Done")

    def backward(self, steps):
        """
        Step the motor backward the given number of steps

        Keyword arguments:
        steps -- an integer number of steps to move
        """
        _LOGGER.debug("Moving backward %r steps", steps)
        for _ in range(steps):
            self._step_backward()
        _LOGGER.debug("Done")

    def _set_sub_step(self, states):
        if len(states) != len(self._coils):
            raise AssertionError(
                "Can't set sub step: number of pin states does not match number"
                "of coils")
        for coil, state in zip(self._coils, states):
            if state:
                coil.on()
            else:
                coil.off()

    def _step_forward(self):
        for state in self._seq:
            self._set_sub_step(state)
            sleep(self._delay / 1000)

    def _step_backward(self):
        for state in reversed(self._seq):
            self._set_sub_step(state)
            sleep(self._delay / 1000)
