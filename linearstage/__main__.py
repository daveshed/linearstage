"""
Entry point for the linear stage application that allows a user to set the
stage position index from the command line.
"""
from logging import getLogger

from linearstage.config import STAGE_CONFIG, setup_logger
from linearstage.stage import Stage

LOGGER = getLogger("linearstage")
STAGE = Stage.from_config(STAGE_CONFIG)
setup_logger()

while True:
    try:
        STAGE.position = int(input("Set position to? "))
    except ValueError:
        LOGGER.exception(
            "Could not parse input. Please supply an integer position")
    except KeyboardInterrupt:
        break
