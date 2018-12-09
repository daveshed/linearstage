from logging import getLogger

from linearstage.config import STAGE_CONFIG, setup_logger
from linearstage.stage import Stage

logger = getLogger("motor")

linearstage = Stage.from_config(STAGE_CONFIG)
setup_logger()

while True:
    position = int(input("Set position to? "))
    linearstage.position = position