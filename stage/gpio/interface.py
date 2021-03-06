"""
I/O interface definitions required by the stage package. These classes serve
as abstractions so that different concrete I/O adaptors can be implemented.
"""
import abc


class OutputInterface(abc.ABC):
    """
    Initialise the given pin as an output on the gpio instance supplied

    Args:
        pin (int): the physical pin to initialise
    """
    def __init__(self, pin: int):
        self._pin = pin
        self._state = None

    @property
    def pin(self):
        """
        The physical pin that this output refers to

        Returns:
            int: the index of the pin this output applies to
        """
        return self._pin

    @property
    def state(self):
        """
        The signal at the output

        Retruns:
            bool: True if the output is high
        """
        return self._state

    @abc.abstractproperty
    def activate(self):
        """
        Set the output high
        """
        return

    @abc.abstractproperty
    def deactivate(self):
        """
        Set the output low
        """
        return

    @abc.abstractproperty
    def gpio(self):
        """
        Returns the gpio driver
        """
        return


class InputInterface(abc.ABC):
    """
    Initialise the given pin as an input

    Args:
        pin (int): the physical pin to use
        active_low (bool): True if the input is active_low ie. a low input
            is interpreted as logical True value
    """
    @abc.abstractmethod
    def __init__(self, pin: int, active_low: bool):
        self._pin = pin
        self._active_low = active_low
        self._state = None

    @property
    def pin(self):
        """
        The physical pin that this input refers to

        Returns:
            int: the index of the pin this input applies to
        """
        return self._pin

    @abc.abstractproperty
    def state(self):
        """
        The current state of the input

        Returns:
            bool: logical value of this input
        """
        return

    @abc.abstractmethod
    def register_callback(self, callback):
        """
        Register a callback to be called in case the input is activated
        """
        return

    @abc.abstractmethod
    def deregister_callback(self, callback):
        """
        Deregister a callback that has already been registered
        """
        return

    @abc.abstractproperty
    def gpio(self):
        """
        Returns the gpio driver
        """
        return
