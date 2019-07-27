"""
Abstraction for a the the stepper motors windings.
"""
from collections import namedtuple

from stage.gpio import GpioBase

_LABELS = ['a1', 'b1', 'a2', 'b2']
State = namedtuple('State', _LABELS)
Pins = namedtuple("Pins", _LABELS)


class Coils:
    def __init__(self, a1, b1, a2, b2):
        self._coils = [a1, b1, a2, b2]

    @classmethod
    def from_pins(cls, pins: Pins, gpio: GpioBase):
        coils = [Coil(label, pin, gpio) for label, pin in zip(_LABELS, pins)]
        return cls(*coils)

    def deactivate(self):
        for coil in self._coils:
            coil.off()

    def set_state(self, state):
        for coil in self._coils:
            output = getattr(state, coil.label)
            if output:
                coil.on()
            else:
                coil.off()


class Coil:
    """
    Drives a single coil within a stepper motor

    Args:
        label (str): the label associated with the pin - refers to datasheet
        pin (int): the number of the gpio pin that activates the coil
        gpio (GpioBase): the gpio object used to control the digital pin to
            to which the winding is connected. It must implement the GpioBase
            interface.
    """
    def __init__(self, label: str, pin: int, gpio: GpioBase):
        self._gpio = gpio
        self._gpio.initialise_output(pin)
        self._pin = pin
        self._label = label
        self._active = False
        self.off()

    @property
    def label(self):
        """
        The label of the pin
        """
        return self._label

    @property
    def active(self):
        """
        The state of the coil

        Returns:
            (bool): the state of the coil
        """
        return self._active

    def on(self):
        """
        Energise the coil
        """
        # pylint: disable=invalid-name
        self._gpio.set_high(self._pin)
        self._active = True

    def off(self):
        """
        De-energise the coil
        """
        self._gpio.set_low(self._pin)
        self._active = False
