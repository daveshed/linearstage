"""
The linear stage module that defines a software driver of a hardware assembly
comprising stepper motor, track and end stop limit switch.
"""

import logging
from time import sleep

from stage import error
from stage.endstop import EndStop
from stage.motor import Motor

_LOGGER = logging.getLogger("STAGE")


class Stage:
    """
    Track controller class. Moves a stepper motor along a linear gear. An end
    stop switch is required at one end (left-hand-side x = 0) to reset the
    position index. The stage must be homed in order to have a meaningful
    position.

    Keyword arguments:
    motor -- a stepper motor instance used to drive the stage
    end_stop -- an end stop instance to inform when the stage has reached its
    home position.
    min_limit -- minimum stage position index
    max_limit -- maximum stage position index
    """
    def __init__(self, motor, end_stop, min_limit, max_limit):
        _LOGGER.info("Instantiating stage")
        self.motor = motor
        self.end_stop = end_stop
        self._min = min_limit
        self._max = max_limit
        # position is undefined at startup. Stage needs to home first.
        self._position = None
        self.home()

    @classmethod
    def from_config(cls, config: dict):
        """
        Returns Stage instance instance from a config dictionary

        Keyword arguments:
        config -- a dictionary that defines the stage's configuration parameters
        """
        motor = Motor.from_config(config['motor'])
        end_stop = EndStop(
            config['end_stop']['pin'],
            config['end_stop']['normally_high']
        )
        return cls(motor, end_stop, config['min_limit'], config['max_limit'])

    def home(self):
        """
        Send the stage to its home position
        """
        _LOGGER.info("Homing stage...")
        while not self.end_stop.triggered:
            self.motor.backward(1)
            sleep(0.01)
        _LOGGER.info("Done")
        self._position = 0
        self.motor.deactivate()

    def end(self):
        """
        Move the stage to its end position
        """
        _LOGGER.info("Stage moving to end stop...")
        self.position = self._max

    @property
    def max(self):
        """
        Returns the maximum stage position index
        """
        return self._max

    @property
    def position(self):
        """
        Get the stage position index
        """
        _LOGGER.info("Reading position...")
        if self._position is None:
            raise AssertionError("Position is undefined. Go to home position")
        return self._position

    @position.setter
    def position(self, request: int):
        """
        Move the stage to the requested position index

        Keyword arguments:
        request -- requested position index
        """
        _LOGGER.info("Moving to position %r...", request)
        if request > self._max or request < self._min:
            raise error.OutOfRangeError("Cannot go to position %d" % request)
        delta = request - self._position
        if delta > 0:
            self.motor.forward(delta)
        else:
            self.motor.backward(delta)
        self.motor.deactivate()
        self._position = request
        _LOGGER.info("Done")
