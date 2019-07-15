"""
Abstraction for a single coil connected to digital gpio. Separating this code
into a module means that RPi.GPIO need not be imported when testing.
"""
import RPi.GPIO as GPIO


class Coil:
    """
    Drives a single coil within a stepper motor

    Args:
        label (str): the label associated with the pin - refers to datasheet
        pin (int): the number of the gpio pin that activates the coil
    """
    def __init__(self, label: str, pin: int):
        GPIO.setup(pin, GPIO.OUT)
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
        GPIO.output(self._pin, 1)
        self._active = True

    def off(self):
        """
        De-energise the coil
        """
        GPIO.output(self._pin, 0)
        self._active = False
