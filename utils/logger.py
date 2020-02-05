import sys
import logging
import settings

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

if settings.debug:
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
