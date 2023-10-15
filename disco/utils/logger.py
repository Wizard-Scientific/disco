import os
import logging

from logging.handlers import TimedRotatingFileHandler
from .config import init_config


def init_logger(filename=None, level=logging.INFO):
    config = init_config()
    logger = logging.getLogger(config["bot_name"])
    
    # only the first invocation will configure this
    if not len(logger.handlers):
        logger.setLevel(level)
        logger.propagate = False

        handler = TimedRotatingFileHandler(filename, when='d', interval=1, backupCount=30)
        monitor_format = logging.Formatter('%(asctime)s %(levelname)-8s p%(process)5s %(module)-15.15s %(message)s')
        handler.setFormatter(monitor_format)
        logger.addHandler(handler)

        logger.debug(f"logging to {filename} at level {logging.getLevelName(level)}")

    return logger
