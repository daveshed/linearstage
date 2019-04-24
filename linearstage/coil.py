"""
The driver for electromagnetic coils connected to digital gpio
"""
import RPi.GPIO as GPIO

# FIXME: these options should be set globally if at all
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Coil:
    """
    A driver for a coil within a stepper motor.

    Keyword arguments:
    pin -- the index of the gpio pin that activates the coil
    """
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        self._pin = pin

    def on(self):
        """
        Energise the coil
        """
        # pylint: disable=invalid-name
        GPIO.output(self._pin, 1)

    def off(self):
        """
        De-energise the coil
        """
        GPIO.output(self._pin, 0)
