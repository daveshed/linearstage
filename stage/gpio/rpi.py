"""
io interface concretions of the stage iointerface that apply to the RPi.GPIO
library.
"""
import RPi.GPIO as RPI_GPIO

from stage.gpio import interface as iointerface
from stage.gpio import error

RPI_GPIO.setmode(RPI_GPIO.BCM)


class OutputChannel(iointerface.OutputInterface):
    """
    Concrete implementation of the OutputInterface abstraction
    """
    _GPIO_DRIVER = RPI_GPIO

    def __init__(self, pin: int):
        """
        Initialise the given pin as an output on the gpio instance supplied

        Args:
            pin (int): the physical pin to initialise
            gpio (RPi.GPIO): the raspberry pi gpio driver instance
        """
        super().__init__(pin)
        self.gpio.setup(pin, self.gpio.OUT)
        self.deactivate()

    def activate(self):
        """
        Set the output high
        """
        self.gpio.output(self._pin, 1)
        self._state = True

    def deactivate(self):
        """
        Set the output low
        """
        self.gpio.output(self._pin, 0)
        self._state = False

    @property
    def gpio(self):
        return type(self)._GPIO_DRIVER


class InputChannel(iointerface.InputInterface):
    """
    Concrete implementation of the InputInterface abstraction
    """
    _DEBOUNCE_MS = 200
    _GPIO_DRIVER = RPI_GPIO

    class CallbackManager:
        #pylint:disable=too-few-public-methods
        """
        Manages callbacks registered with the gpio instance
        """
        def __init__(self):
            self.callbacks = []

        def __call__(self, *args, **kwargs):
            for callback in self.callbacks:
                callback(args, kwargs)

    def __init__(self, pin: int, active_low: bool):
        """
        Initialise the given pin as an input on the gpio instance supplied

        Args:
            pin (int): the physical pin to use
            active_low (bool): True if the input is active_low ie. a low input
                is interpreted as logical True value
        """
        super().__init__(pin, active_low)
        self._callback_manager = type(self).CallbackManager()
        self.gpio.setup(
            pin,
            self.gpio.IN,
            self.gpio.PUD_UP if active_low else self.gpio.PUD_DOWN)
        self.gpio.add_event_detect(
            pin,
            self.gpio.FALLING if active_low else self.gpio.RISING,
            callback=self._callback_manager,
            bouncetime=type(self)._DEBOUNCE_MS)

    @property
    def state(self):
        """
        The current logical state of the input

        Returns:
            bool: True if the input is recieving a logical high value at the
                present moment
        """
        signal = bool(self.gpio.input(self._pin))
        logic_level = not signal if self._active_low else signal
        return logic_level

    def register_callback(self, callback):
        """
        Register a callback to be called when the input is activated
        """
        self._callback_manager.callbacks.append(callback)

    def deregister_callback(self, callback):
        """
        Deregister a callback that has already been registered
        """
        try:
            self._callback_manager.callbacks.remove(callback)
        except ValueError:
            raise error.GpioError(
                "Cannot deregister %r. Not registered" % callback)

    @property
    def gpio(self):
        return type(self)._GPIO_DRIVER
