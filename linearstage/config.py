import logging
from sys import stdout

def setup_logger():
    logging.basicConfig(
        format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
        stream=stdout,
        level=logging.INFO)

COIL_A1_PIN = 13 # pink
COIL_A2_PIN = 26 # orange
COIL_B1_PIN = 6  # blue
COIL_B2_PIN = 19 # yellow

SEQUENCE = [
    [0,1,0,0],
    [0,1,0,1],
    [0,0,0,1],
    [1,0,0,1],
    [1,0,0,0],
    [1,0,1,0],
    [0,0,1,0],
    [0,1,1,0]
]

MS_DELAY = 10

END_STOP_PIN = 22

MAX_STAGE_LIMIT = 4400
MIN_STAGE_LIMIT = 0