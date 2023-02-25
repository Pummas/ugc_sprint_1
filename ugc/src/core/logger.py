import logging
import logging.config as logging_config
from contextvars import ContextVar
from typing import Any

from core.config import settings

_log_extra_info: ContextVar[dict] = ContextVar("_log_extra_info")


def set_log_extra(log_extra: dict[str, Any]):
    """Сохранить дополнительную информацию для логирования."""
    _log_extra_info.set(log_extra)


def get_log_extra() -> dict[str, Any] | None:
    """Получить дополнительную информацию для логирования."""
    return _log_extra_info.get(None)


class ExtraContextInfoLogger(logging.getLoggerClass()):
    """Логгер, который добавляет дополнительную информацию из контекста.

    Если при логировании передать дополнительный словарь в параметре extra,
    то при совпадении ключей информация из контекста имеет приоритет.
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name=name)

    def _log(self, *args, extra=None, **kwargs):
        extra_info = get_log_extra()
        if extra is not None and extra_info is not None:
            extra_info = extra | extra_info

        super()._log(*args, extra=extra_info, **kwargs)


class UvicornAccessStreamHandler(logging.StreamHandler):
    """Обработчик для логов uvicorn.access.

    Добавляет в атрибуты LogRecord данные, которые uvicorn использует
    для access-логов.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def emit(self, record):
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


# you can easy enable log file
LOG_FILE = "/dev/null"

if settings.DEBUG:
    LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(funcName)s %(lineno)d)"
    LOG_LEVEL = logging.DEBUG
else:
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_LEVEL = logging.INFO

LOG_DEFAULT_HANDLERS = ["console", "file"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app_default": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": LOG_FORMAT,
        },
        "uvicorn_default": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
        "uvicorn_access": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": (
                "%(asctime)s %(name)s %(levelname)s"
                "%(client_addr)s %(method)s %(full_path)s %(http_version)s %(status_code)s"
            ),
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "app_default",
        },
        "uvicorn_default": {
            "formatter": "uvicorn_default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
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
            "handlers": ["uvicorn_default"],
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
    },
    "root": {
        "level": LOG_LEVEL,
        "formatter": "app_default",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}

logging.setLoggerClass(ExtraContextInfoLogger)
logging_config.dictConfig(LOGGING)
