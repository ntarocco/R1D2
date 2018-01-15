import logging
from os import getenv

logging.basicConfig(
    level=getenv('R1D2_LOGGING_LEVEL', logging.INFO),
    format="[%(asctime)s] %(levelname)s %(message)s"
)

logger = logging.getLogger()
