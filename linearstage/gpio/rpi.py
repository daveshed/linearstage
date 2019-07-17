import RPi.GPIO as GPIO

from linearstage.gpio.base import GpioBase

GPIO.setmode(GPIO.BCM)
# The GPIO.BOARD option specifies that you are referring to the pins by the
# number of the pin the the plug - i.e the numbers printed on the board
# (e.g. P1) and in the middle of the diagrams below.
# The GPIO.BCM option means that you are referring to the pins by the "Broadcom
# SOC channel" number, these are the numbers after "GPIO" in the green
# rectangles around the outside of the below diagrams.

class RPiGpio(GpioBase):
    """
    https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    """
    @staticmethod
    def initialise_output(pin: int):
        GPIO.setup(pin, GPIO.OUT)

    @staticmethod
    def initialise_input(
            pin: int,
            active_low: bool,
            event_callback=None):
        GPIO.setup(
            pin,
            GPIO.IN,
            GPIO.PUD_UP if active_low else GPIO.PUD_DOWN)
        if event_callback:
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING if active_low else GPIO.RISING,
                callback=event_callback)

    @staticmethod
    def set_high(pin: int):
        GPIO.output(pin, 1)        

    @staticmethod
    def set_low(pin: int):
        GPIO.output(pin, 0)        

    @staticmethod
    def input_triggered(pin):
        return bool(GPIO.input(pin))

    @staticmethod
    def clean_up():
        GPIO.cleanup()
