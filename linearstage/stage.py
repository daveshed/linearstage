import logging
from time import sleep
from sys import stdout

from linearstage.config import (
    COIL_A1_PIN,
    COIL_A2_PIN,
    COIL_B1_PIN,
    COIL_B2_PIN,
    END_STOP_PIN,
    MIN_STAGE_LIMIT,
    MAX_STAGE_LIMIT,
    SEQUENCE,
    setup_logger,
)
from linearstage.endstop import EndStop
from linearstage.motor import Motor


logger = logging.getLogger("stage")


class OutOfRangeError(Exception):
    pass

class TimeOutError(Exception):
    pass


class Stage:
    """
    Track controller class. Moves a stepper motor along a linear gear. An end
    stop switch is required at one end (left-hand-side x = 0) to reset the
    position index. The stage must be homed in order to have a meaningful
    position.
    """    
    def __init__(self, motor, end_stop):
        logger.info("Instantiating stage")
        self.motor = motor
        self.end_stop = end_stop
        # position is undefined at startup. Stage needs to home first.
        self._position = None
        self.home()

    def home(self):
        logger.info("Homing stage...")
        while not self.end_stop.triggered:
            self.motor.backward(1)
            sleep(0.01)
        logger.info("Done")
        self._position = 0
        self.motor.deactivate()

    def end(self):
        logger.info("Stage moving to end stop...")
        self.position = MAX_STAGE_LIMIT

    @property
    def position(self):
        logger.info("Reading position...")
        if self._position is None:
            raise AssertionError("Position is undefined. Go to home position")
        return self._position

    @position.setter
    def position(self, request):
        logger.info("Moving to position {}...".format(request))
        if request > MAX_STAGE_LIMIT or request < MIN_STAGE_LIMIT:
                raise OutOfRangeError("Cannot go to position {}"
                    .format(request))
        delta = request - self._position
        if delta > 0:
            self.motor.forward(delta)
        else:
            self.motor.backward(delta)
        self.motor.deactivate()
        self._position = request
        logger.info("Done")


if __name__ == '__main__':
    setup_logger()
    endstop = EndStop(END_STOP_PIN)
    motor = Motor(
        pins=[
            COIL_A1_PIN,
            COIL_A2_PIN,
            COIL_B1_PIN,
            COIL_B2_PIN,
        ],
        sequence=SEQUENCE)
    linearstage = Stage(motor, endstop)