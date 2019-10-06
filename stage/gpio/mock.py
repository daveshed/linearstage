"""
Mock concrete implementations of iointerface defined by the stage package
"""
from stage.gpio import interface as iointerface
from stage.gpio import error


class OutputChannel(iointerface.OutputInterface):
    """
    Mock concrete implementation of iointerface defined by the stage package
    """
    _GPIO_DRIVER = None

    def activate(self):
        """
        Set the output high
        """
        self._state = True
        return self.state

    def deactivate(self):
        """
        Set the output low
        """
        self._state = False
        return self.state

    def gpio(self):
        """
        Returns the gpio driver
        """
        return type(self)._GPIO_DRIVER


class InputChannel(iointerface.InputInterface):
    #pylint:disable=too-few-public-methods
    """
    Mock concrete implementation of iointerface defined by the stage package
    """
    _GPIO_DRIVER = None

    def __init__(self, pin: int, active_low: bool):
        """
        Initialise the given pin as an input

        Args:
            pin (int): the physical pin to use
            active_low (bool): True if the input is active_low ie. a low input
                is interpreted as logical True value
        """
        super().__init__(pin, active_low)
        self._state = False
        self._pin = pin
        self._callbacks = []

    @property
    def state(self):
        """
        The current logical state of the input

        Returns:
            bool: True if the input is recieving a logical high value at the
                present moment
        """
        return self._state

    def register_callback(self, callback):
        """
        Register a callback to be called in case the input is activated
        """
        self._callbacks.append(callback)

    def deregister_callback(self, callback):
        """
        Deregister a callback that has already been registered
        """
        try:
            self._callbacks.remove(callback)
        except ValueError:
            raise error.GpioError(
                "Cannot deregister %r. Not registered" % callback)

    def activate(self):
        """
        Called by tests to set the state of the input externally - sets the
        logical state of the input to True

        Args:
            state (bool): the logical value to set the input to
        """
        self._state = True
        self._invoke_callbacks()

    def deactivate(self):
        """
        Called by tests to set the state of the input externally - Sets the
        logical state of the input to False

        Args:
            state (bool): the logical value to set the input to
        """
        self._state = False

    def _invoke_callbacks(self):
        for callback in self._callbacks:
            callback()

    def gpio(self):
        """
        Returns the gpio driver
        """
        return type(self)._GPIO_DRIVER
