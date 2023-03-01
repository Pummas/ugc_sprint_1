import logging
import logging.config as logging_config
import time
from contextvars import ContextVar
from typing import Any, AnyStr, Dict, Optional

from pythonjsonlogger.jsonlogger import JsonFormatter

from core.config import settings

_log_extra_info: ContextVar[Dict[AnyStr, Any]] = ContextVar("_log_extra_info")


def set_log_extra(log_extra: Dict[AnyStr, Any]):
    """Сохранить дополнительную информацию для логирования."""
    _log_extra_info.set(log_extra)


def get_log_extra() -> Optional[Dict[AnyStr, Any]]:
    """Получить дополнительную информацию для логирования."""
    return _log_extra_info.get(None)


class ExtraContextInfoLogger(logging.getLoggerClass()):
    """Логгер, который добавляет дополнительную информацию из контекста.

    Если при логировании передать дополнительный словарь в параметре extra,
    то при совпадении ключей информация из контекста имеет приоритет.
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name=name)

    def _log(self, *args, extra: Optional[Dict[AnyStr, Any]] = None, **kwargs):
        extra_info = get_log_extra()
        if extra is not None and extra_info is not None:
            extra_info = extra | extra_info

        super()._log(*args, extra=extra_info, **kwargs)


class UvicornAccessStreamHandler(logging.StreamHandler):
    """Обработчик для логов uvicorn.access.

    Добавляет в атрибуты LogRecord данные, которые uvicorn использует
    для access-логов.
    """

    def emit(self, record: logging.LogRecord):
        if record.name == "uvicorn.access":
            client_addr, method, full_path, http_version, status_code = record.args
            record.__dict__.update(
                {
                    "client_addr": client_addr,
                    "method": method,
                    "full_path": full_path,
                    "http_version": http_version,
                    "status_code": status_code,
                }
            )
        super().emit(record)


class MsecTimeJsonFormatter(JsonFormatter):
    """Добавляет в формат даты-времени параметр %F для миллисекунд."""

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[AnyStr] = None):
        if datefmt is None:
            return super().formatTime(record, datefmt=None)

        if "%F" in datefmt:
            msec = "%03d" % record.msecs
            datefmt = datefmt.replace("%F", msec)

        ct = self.converter(record.created)
        return time.strftime(datefmt, ct)


# you can easy enable log file
LOG_FILE = "/dev/null"

if settings.DEBUG:
    LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(funcName)s %(lineno)d)"
    LOG_LEVEL = logging.DEBUG
else:
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_LEVEL = logging.INFO

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%F%z"  # ISO8601, %F - миллисекунды

LOG_DEFAULT_HANDLERS = ["console", "file"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app_default": {
            "()": MsecTimeJsonFormatter,
            "fmt": LOG_FORMAT,
            "datefmt": DATE_FORMAT,
        },
        "uvicorn_access": {
            "()": MsecTimeJsonFormatter,
            "fmt": (
                "%(asctime)s %(name)s %(levelname)s"
                "%(client_addr)s %(method)s %(full_path)s %(http_version)s %(status_code)s"
            ),
            "datefmt": DATE_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "app_default",
        },
        "uvicorn_access": {
            "formatter": "uvicorn_access",
            "()": UvicornAccessStreamHandler,
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "app_default",
            "filename": LOG_FILE,
            "mode": "w",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["uvicorn_access"],
            "level": "INFO",
            "propagate": False,
        },
        "backoff": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "formatter": "app_default",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}

logging.setLoggerClass(ExtraContextInfoLogger)
logging_config.dictConfig(LOGGING)
