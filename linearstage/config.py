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

END_STOP_PIN = 22

MOTOR_CONFIG = {
    'pins': [COIL_A1_PIN, COIL_A2_PIN, COIL_B1_PIN, COIL_B2_PIN],
    'sequence': SEQUENCE,
    'ms_delay': 10,
}

STAGE_CONFIG = {
    'end_stop': {'pin': END_STOP_PIN, 'normally_high': True},
    'motor': MOTOR_CONFIG,
    'min_limit': 0,
    'max_limit': 4400,
}