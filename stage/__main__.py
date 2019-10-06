"""
Entry point for the stage application that allows a user to set the stage
position index from the command line.
"""
import logging
import sys

from stage.stage import Stage
from stage.factory.config import Configurator
from stage.factory.rpi import RPiMonopolarStepperStageFactory


logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=sys.stdout,
    level=logging.INFO)

LOGGER = logging.getLogger("linearstage")
CONFIG = Configurator(
    motor_pins=(
        26, # a1 orange
        19, # b1 yellow
        13, # a2 pink
        6,  # b2 blue
    ),
    end_stop_pin=22,
    end_stop_active_low=True,
    maximum_position=4400,
    minimum_position=0)
STAGE = Stage(RPiMonopolarStepperStageFactory(CONFIG))

while True:
    try:
        STAGE.position = int(input("Set position to? "))
    except ValueError:
        LOGGER.exception(
            "Could not parse input. Please supply an integer position")
    except KeyboardInterrupt:
        break
