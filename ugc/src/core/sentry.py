import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from core.config import settings


def before_send(event, hint):
    # не отправляем в sentry сообщения об ошибках из логов aiokafka
    if event.get("logger", None) == "aiokafka":
        return None
    return event


def init_sentry():
    if settings.ENABLE_SENTRY:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            debug=settings.DEBUG,
            release=settings.RELEASE_VERSION,
            request_bodies="medium",
            sample_rate=1.0,
            traces_sample_rate=0.0,
            before_send=before_send,
            integrations=[LoggingIntegration(event_level=None)],
        )