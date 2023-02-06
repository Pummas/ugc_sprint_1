import socket

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    TOPIC_NAMES: list[str] = ["views"]
    GROUP_ID: str = "etl_kafka"
    AUTO_OFFSET_RESET: str = "smallest"
    CLIENT_ID: str = Field(default_factory=socket.gethostname)


settings = Settings()

consumer_config = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
    "group.id": settings.GROUP_ID,
    "auto.offset.reset": settings.AUTO_OFFSET_RESET,
}
producer_config = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
    "client.id": socket.gethostname(),
}
admin_config = {
    "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
}
