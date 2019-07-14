"""
The driver for electromagnetic coils connected to digital gpio
"""
import RPi.GPIO as GPIO


class Coils:

    def __init__(self, a1_pin: int, a2_pin: int, b1_pin: int, b2_pin: int):
        self._coils = [Coil(a1_pin), Coil(b1_pin), Coil(a2_pin), Coil(b2_pin)]

    def deactivate(self):
        for coil in self._coils:
            coil.off()

    def set_state(self, state: list):
        for output, coil in zip(state, self._coils):
            if output:
                coil.on()
            else:
                coil.off()


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
