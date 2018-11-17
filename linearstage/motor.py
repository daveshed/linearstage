# code originally inspired by ...
# https://github.com/christophrumpel/test_stepper
# https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/
from time import sleep
from logging import getLogger

from linearstage.coil import Coil
from linearstage.config import (
    COIL_A1_PIN,
    COIL_A2_PIN,
    COIL_B1_PIN,
    COIL_B2_PIN,
    MS_DELAY,
    SEQUENCE,
)


logger = getLogger("motor")

class Motor:

    def __init__(self, pins, sequence):
        logger.info("Instantiated on pins {}".format(pins))
        self._coils = [Coil(pin) for pin in pins]
        self._seq = sequence

    def _set_sub_step(self, states):
        if len(states) != len(self._coils):
            raise AssertionError(
                "Can't set sub step: number of pin states does not match number"
                "of coils")
        for coil, state in zip(self._coils, states):
            if state:
                coil.on()
            else:
                coil.off()

    def _step_forward(self):
        for state in self._seq:
            self._set_sub_step(state)
            sleep(MS_DELAY / 1000)

    def _step_backward(self):
        for state in reversed(self._seq):
            self._set_sub_step(state)
            sleep(MS_DELAY / 1000)

    def deactivate(self):
        logger.info("Deactivating coils")
        [coil.off() for coil in self._coils]

    def forward(self, steps):
        logger.info("Moving forward {} steps".format(steps))
        for i in range(steps):
            self._step_forward()
        logger.info("Done")

    def backward(self, steps):
        logger.info("Moving backward {} steps".format(steps))
        for i in range(steps):
            self._step_backward()
        logger.info("Done")

if __name__ == '__main__':
    motor = Motor(
    pins=[
        COIL_A1_PIN,
        COIL_A2_PIN,
        COIL_B1_PIN,
        COIL_B2_PIN,
    ],
    sequence=SEQUENCE)
    while True:
        steps = int(input("How many steps forward? "))
        motor.forward(steps)
        steps = int(input("How many steps backwards? "))
        motor.backward(steps)
