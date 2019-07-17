"""
Entry point for the stage application that allows a user to set the stage
position index from the command line.
"""
import logging

from linearstage.stage import StageBuilder
from linearstage.gpio.rpi import RPiGpio

logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    stream=stdout,
    level=logging.INFO)

LOGGER = getLogger("linearstage")
STAGE = (
    StageBuilder()
        .build_gpio(RPiGpio)
        .build_coils(
            a1_pin=26, # orange
            b1_pin=19, # yellow
            a2_pin=13, # pink
            b2_pin=6)  # blue
        .build_motor(drive_scheme='Half Step', ms_delay=10)
        .build_end_stop(pin=22, active_low=True)
        .build_track(min_limit=0, max_limit=4400)
        .build_linear_stage()
        .get_stage())

while True:
    try:
        STAGE.position = int(input("Set position to? "))
    except ValueError:
        LOGGER.exception(
            "Could not parse input. Please supply an integer position")
    except KeyboardInterrupt:
        break
