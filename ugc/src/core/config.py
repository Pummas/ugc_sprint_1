from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR.parent / ".env.local"


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("UGC Movies", env="UGC_PROJECT_NAME")
    DEBUG: bool = Field(True, env="UGC_DEBUG")
    JWT_SECRET_KEY: str = Field("secret_jwt_key", env="UGC_JWT_KEY")
    MOCK_AUTH_TOKEN: bool = Field(
        False, env="UGC_MOCK_AUTH_TOKEN"
    )  # для отладки - можно отключить проверку токена в заголовках
    JAEGER_HOST_NAME: str = Field("localhost", env="JAEGER_HOST_NAME")
    JAEGER_PORT: int = Field(6831, env="JAEGER_PORT")
    ENABLE_TRACER: bool = Field(False, env="ENABLE_TRACER")

    KAFKA_INSTANCE: str = Field("localhost:39092", env="UGC_KAFKA_INSTANCE")

    MONGO_URL: str = Field(
        "mongodb://user_name:user_password@localhost:27017/prod-db?authSource=admin", env="UGC_MONGO_URL"
    )
    MONGO_DB: str = Field("prod-db", ENV="MONGO_DB")

    ENABLE_SENTRY: bool = Field(False, env="ENABLE_SENTRY")
    SENTRY_DSN: str = Field("<sentry dsn>", env="SENTRY_DSN")
    RELEASE_VERSION: str = Field("ugc-service@1.0.0", env="RELEASE_VERSION")


settings = Settings(_env_file=ENV_FILE)
