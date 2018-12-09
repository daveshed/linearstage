import logging
from time import sleep
from sys import stdout

from linearstage.config import STAGE_CONFIG
from linearstage.motor import Motor
from linearstage.endstop import EndStop

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
    def __init__(self, motor, end_stop, min_limit, max_limit):
        logger.info("Instantiating stage")
        self.motor = motor
        self.end_stop = end_stop
        self._min = min_limit
        self._max = max_limit
        # position is undefined at startup. Stage needs to home first.
        self._position = None
        self.home()

    @classmethod
    def from_config(cls, config: dict):
        motor = Motor.from_config(config['motor'])
        end_stop = EndStop(
            config['end_stop']['pin'],
            config['end_stop']['normally_high']
        )
        return cls(motor, end_stop, config['min_limit'], config['max_limit'])

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
        self.position = self._max

    @property
    def max(self):
        return self._max

    @property
    def position(self):
        logger.info("Reading position...")
        if self._position is None:
            raise AssertionError("Position is undefined. Go to home position")
        return self._position

    @position.setter
    def position(self, request):
        logger.info("Moving to position {}...".format(request))
        if request > self._max or request < self._min:
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