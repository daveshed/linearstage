import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Coil:
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        self._pin = pin
        
    def on(self):
        GPIO.output(self._pin, 1)

    def off(self):
        GPIO.output(self._pin, 0)