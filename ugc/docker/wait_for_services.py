import logging.config
import os

import backoff
from confluent_kafka.admin import AdminClient, KafkaException

KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:39092")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": logging.DEBUG,
        "formatter": "default",
        "handlers": ["default"],
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def fake_send_email(details: dict):
    logger.debug("Send email")


@backoff.on_predicate(backoff.expo, logger=logger, max_time=300, on_giveup=fake_send_email, max_value=5)
def check_kafka(admin_client: AdminClient) -> bool:
    try:
        admin_client.list_topics()
        return True
    except KafkaException:
        return False


def wait():
    kafka_client = AdminClient({"bootstrap.servers": KAFKA_SERVERS})
    logger.info("Waiting for Kafka")
    check_kafka(kafka_client)
    logger.info("Kafka is up")


if __name__ == "__main__":
    wait()
