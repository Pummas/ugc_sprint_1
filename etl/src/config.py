import socket

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:39092,localhost:39093,localhost:39094"
    CLICKHOUSE_HOST: str = "localhost"
    DEBUG: bool = Field(False, env="ETL_KAFKA_DEBUG")
    MAX_BATCH_SIZE: int = Field(1000, env="ETL_KAFKA_RECORDS_PER_BATCH")
    TOPIC_NAMES: list[str] = ["user.views"]
    GROUP_ID: str = "etl_kafka"
    AUTO_OFFSET_RESET: str = "smallest"


settings = Settings()

consumer_config = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
    "group.id": settings.GROUP_ID,
    "auto.offset.reset": settings.AUTO_OFFSET_RESET,
    "enable.auto.offset.store": False,
}
producer_config = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
    "client.id": socket.gethostname(),
}
admin_config = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
}
