"""
End stop for informing the stage when it has reached the end of its travel
"""
from logging import getLogger

import RPi.GPIO as GPIO

_LOGGER = getLogger("end stop")


class EndStop:
    """
    An end stop switch that triggers when the stage comes into contact

    Keyword arguments:
    pin -- the digital pin that the stop is wired to
    normally_high -- the normal state of the endstop ie when not triggered
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, pin: int, normally_high: bool):
        if normally_high:
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
            self._inverted = True
            _LOGGER.info("Initialised end stop on pin %d high", pin)
        else:
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
            self._inverted = False
            _LOGGER.info("Initialised end stop on pin %d low", pin)
        self._pin = pin

    @property
    def triggered(self):
        """
        Returns the state of the end stop
        """
        state = bool(GPIO.input(self._pin))
        if self._inverted:
            triggered = not state
        else:
            triggered = state
        _LOGGER.debug("End stop triggered: %r", triggered)
        return triggered
