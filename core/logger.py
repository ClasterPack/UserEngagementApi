import logging
import logstash
from core.config import settings


def get_logger():
    logger = logging.getLogger("api_logger")
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    logstash_handler = logstash.LogstashHandler(settings.logstash, 5044, version=1)
    logger.addHandler(logstash_handler)

    return logger
