# code originally inspired by ...
# https://github.com/christophrumpel/test_stepper
# https://tutorials-raspberrypi.com/how-to-control-a-stepper-motor-with-raspberry-pi-and-l293d-uln2003a/
from time import sleep
from logging import getLogger

from linearstage.coil import Coil


logger = getLogger("motor")

class Motor:

    def __init__(self, pins, sequence, ms_delay):
        logger.info("Instantiated on pins {}".format(pins))
        self._coils = [Coil(pin) for pin in pins]
        self._seq = sequence
        self._delay = ms_delay

    @classmethod
    def from_config(cls, config: dict):
        return cls(
            config['pins'],
            config['sequence'],
            config['ms_delay']
        )

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
            sleep(self._delay / 1000)

    def _step_backward(self):
        for state in reversed(self._seq):
            self._set_sub_step(state)
            sleep(self._delay / 1000)

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