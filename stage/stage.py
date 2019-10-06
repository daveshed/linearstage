"""
The linear stage module that defines a software driver of a hardware assembly
comprising stepper motor, track and end stop limit switch.
"""

import logging
import threading

from stage.motor import coil
from stage import exceptions
from stage import endstop
from stage import motor
from stage.factory.base import StageFactoryBase

_LOGGER = logging.getLogger("STAGE")


class Stage:
    """
    Track controller class. Moves a stepper motor along a linear gear. An end
    stop switch is required at one end (left-hand-side x = 0) to reset the
    position index. The stage must be homed in order to have a meaningful
    position.

    Keyword arguments:
        factory ....
    """
    def __init__(self, factory: StageFactoryBase):
        _LOGGER.info("Instantiating stage using factory %r" % factory)
        self.motor = factory.motor
        self.end_stop = factory.end_stop
        self.end_stop.register_callback(self._handle_end_stop_triggered)
        self._min = factory.minimum_position
        self._max = factory.maximum_position
        self._at_home_position = threading.Event()
        # position is undefined at startup. Stage needs to home first.
        self._position = None
        self.home()

    def home(self):
        """
        Send the stage to its home position
        """
        _LOGGER.info("Homing stage...")
        # TODO: timeout needed here. what if the stage is stuck or endstop
        # broken
        if not self.end_stop.triggered:
            while not self._at_home_position.is_set():
                self.motor.backward(1)
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
    def min(self):
        """
        Returns the minimum stage position index
        """
        return self._min

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
        _LOGGER.debug("Reading position...")
        return self._position

    @position.setter
    def position(self, request: int):
        """
        Move the stage to the requested position index

        Keyword arguments:
        request -- requested position index
        """
        _LOGGER.info("Moving to position %r...", request)
        self._goto_request(request)
        self._position = request
        self._at_home_position.clear()
        _LOGGER.info("Done")

    def _handle_end_stop_triggered(self):
        _LOGGER.info("End stop triggered")
        self._at_home_position.set()

    def _goto_request(self, request):
        if request > self._max or request < self._min:
            raise exceptions.OutOfRangeError("Cannot go to position %d" % request)
        delta = request - self._position
        if delta > 0:
            self.motor.forward(delta)
        else:
            self.motor.backward(delta)
        self.motor.deactivate()
