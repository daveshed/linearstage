"""
Entry point for the stage application that allows a user to set the stage
position index from the command line.
"""
from logging import getLogger

from stage.config import STAGE_CONFIG, setup_logger
from stage.stage import Stage

LOGGER = getLogger("STAGE")
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
