"""
End stop for informing the stage when it has reached the end of its travel
"""
from logging import getLogger

from stage.gpio.interface import InputInterface

_LOGGER = getLogger("END STOP")


class EndStop:
    """
    An end stop switch that triggers when the stage comes into contact

    Args:
        pin (int): the digital pin/channel that the stop is wired to
        active_low (bool): designates the voltage level when the end stop is
            activated eg. active_low=True implies the signal is normally high
            (logic 0) and will go low when triggered (logic 1).
        digital_input (InputInterface): the input interface object
    """
    # pylint: disable=too-few-public-methods
    def __init__(
            self,
            digital_io: InputInterface):
        self._input = digital_io
        self._callbacks = []
        _LOGGER.info("Initialised end stop %r, with %r", self, self._input)

    @property
    def input(self):
        """
        The digital input used by the end stop switch

        Returns:
            int: the pin index
        """
        return self._input

    @property
    def triggered(self):
        """
        The state of the end stop

        Returns:
            bool: True if the end stop is triggered at this instant
        """
        _LOGGER.debug("End stop %r triggered: %r", self, self._input.state)
        return self._input.state

    def register_callback(self, callback):
        """
        Register a callback to be called when the endstop is triggered.

        Args:
            callback (obj): the function to be registered
        """
        self._input.register_callback(callback)

    def deregister_callback(self, callback):
        """
        Deregister the given callback

        Args:
            callback (obj): the function to be deregistered
        """
        self._input.deregister_callback(callback)

    def _handle_triggered_event(self):
        for callback in self._callbacks:
            callback()
