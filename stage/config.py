"""
Configuration file for the linear stage based on...
5V Stepper Motor 28BYJ-48 With Drive Test Module Board ULN2003 5 Line 4 Phase
with microswitch endstop.
"""
import logging
from sys import stdout

import RPi.GPIO as GPIO
# The GPIO.BOARD option specifies that you are referring to the pins by the
# number of the pin the the plug - i.e the numbers printed on the board
# (e.g. P1) and in the middle of the diagrams below.
# The GPIO.BCM option means that you are referring to the pins by the "Broadcom
# SOC channel" number, these are the numbers after "GPIO" in the green
# rectangles around the outside of the below diagrams.
GPIO.setmode(GPIO.BCM)

def setup_logger():
    """Basic logger configuration"""
    logging.basicConfig(
        format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
        stream=stdout,
        level=logging.INFO)

COIL_A1_PIN = 26 # orange
COIL_B1_PIN = 19 # yellow
COIL_A2_PIN = 13 # pink
COIL_B2_PIN = 6  # blue

SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]

END_STOP_PIN = 22

MOTOR_CONFIG = {
    'pins': [COIL_A1_PIN, COIL_B1_PIN, COIL_A2_PIN, COIL_B2_PIN],
    'sequence': SEQUENCE,
    'ms_delay': 10,
}

STAGE_CONFIG = {
    'end_stop': {'pin': END_STOP_PIN, 'normally_high': True},
    'motor': MOTOR_CONFIG,
    'min_limit': 0,
    'max_limit': 4400,
}
