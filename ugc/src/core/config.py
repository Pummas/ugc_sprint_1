from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR.parent / ".env.local"


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("UGC Movies", env="UGC_PROJECT_NAME")
    DEBUG: bool = Field(True, env="UGC_DEBUG")
    JWT_SECRET_KEY: str = Field(..., env="UGC_JWT_KEY")
    MOCK_AUTH_TOKEN: bool = Field(
        False, env="UGC_MOCK_AUTH_TOKEN"
    )  # для отладки - можно отключить проверку токена в заголовках
    JAEGER_HOST_NAME: str = Field(..., env="JAEGER_HOST_NAME")
    JAEGER_PORT: int = Field(..., env="JAEGER_PORT")
    ENABLE_TRACER: bool = Field(False, env="ENABLE_TRACER")

    KAFKA_INSTANCE: str = Field("localhost:39092", env="UGC_KAFKA_INSTANCE")

    SENTRY_DSN: str
    SENTRY_AUTH_TOKEN: str
    SENTRY_ORG: str
    SENTRY_PROJECT: str
    RELEASE_VERSION: str
    ENVIRONMENT: str


settings = Settings(_env_file=ENV_FILE)
