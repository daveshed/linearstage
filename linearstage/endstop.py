import RPi.GPIO as GPIO

import logging
logger = logging.getLogger("end stop")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class EndStop:

    def __init__(self, pin, pull_up_down=GPIO.PUD_UP):
        # Set the pin to be an input pin and set initial value to be pulled low
        GPIO.setup(
            pin,
            GPIO.IN,
            pull_up_down)
        logger.info("Initialised end stop on pin {}".format(pin)) 
        self._pin = pin

    @property
    def triggered(self):
        state = not(bool(GPIO.input(self._pin)))
        logger.info("End stop triggered {}".format(state))
        return state