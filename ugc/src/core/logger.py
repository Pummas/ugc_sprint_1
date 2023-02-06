import logging
import logging.config as logging_config

from src.core.config import settings

LOG_FILE = "log.txt"

if settings.DEBUG:
    LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s -- (%(filename)s).%(funcName)s(%(lineno)d)"
    LOG_LEVEL = logging.DEBUG
else:
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = logging.INFO

LOG_DEFAULT_HANDLERS = ["console", "file"]

# В логгере настраивается логгирование uvicorn-сервера.
# Про логирование в Python можно прочитать в документации
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
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
        "file": {"class": "logging.FileHandler", "formatter": "verbose", "filename": LOG_FILE, "mode": "w"},
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": LOG_LEVEL,
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}

logging_config.dictConfig(LOGGING)
