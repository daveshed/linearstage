import RPi.GPIO as GPIO

import logging
logger = logging.getLogger("end stop")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class EndStop:

    def __init__(self, pin, normally_high: bool):
        """An end stop switch that triggers when the stage comes into contact

        Keyword arguments:
        pin -- the digital pin that the stop is wired to
        normally_high -- the normal state of the endstop ie when not triggered
        """
        if normally_high:
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
            self._inverted = True
            logger.info("Initialised end stop on pin {} high".format(pin)) 
        else:
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
            self._inverted = False
            logger.info("Initialised end stop on pin {} low".format(pin)) 
        self._pin = pin

    @property
    def triggered(self):
        state = bool(GPIO.input(self._pin))
        if self._inverted:
            triggered = not(state)
        else:
            triggered = state
        logger.info("End stop triggered {}".format(triggered))
        return triggered