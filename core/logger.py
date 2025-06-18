import logging
import os
import uuid

from core.config import settings
from core.context import ctx_request_id


def setup_root_logger():
    logger = logging.getLogger("")
    if logger.hasHandlers():
        logger.handlers.clear()
    formatter = logging.Formatter(settings.log_format)
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not os.path.exists(settings.logger_filename):
        open(settings.logger_filename, "w").close()

    file = logging.handlers.RotatingFileHandler(
        filename=settings.logger_filename,
        mode=settings.logger_mod,
        maxBytes=settings.logger_maxbytes,
        backupCount=settings.logger_backup_count,
    )
    file.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file)
    logger.setLevel(logging.INFO)

    factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = factory(*args, **kwargs)
        record.request_id = ctx_request_id.get(uuid.uuid4())
        return record

    logging.setLogRecordFactory(record_factory)


LOG_DEFAULT_HANDLERS = ["console"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": settings.log_format},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": LOG_DEFAULT_HANDLERS, "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}

logger = logging.getLogger("posts_logger")
