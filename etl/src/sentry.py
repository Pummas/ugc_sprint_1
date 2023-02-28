import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from config import settings


def init_sentry():
    if settings.ENABLE_SENTRY:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            debug=settings.DEBUG,
            release=settings.RELEASE_VERSION,
            request_bodies="medium",
            sample_rate=1.0,
            traces_sample_rate=0.0,
            integrations=[LoggingIntegration(event_level=None)],
        )
