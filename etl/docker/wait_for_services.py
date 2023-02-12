import logging.config
import os

import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import Error as ClickhouseError
from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient

KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:39092")
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")


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
def check_clickhouse(clickhouse_client: Client) -> bool:
    try:
        clickhouse_client.execute("SHOW DATABASES")
        return True
    except ClickhouseError:
        return False


@backoff.on_predicate(backoff.expo, logger=logger, max_time=300, on_giveup=fake_send_email, max_value=5)
def check_kafka(admin_client: AdminClient) -> bool:
    try:
        admin_client.list_topics()
        return True
    except KafkaException:
        return False


def wait():
    clickhouse_client = Client(host=CLICKHOUSE_HOST)
    logger.info("Waiting for Clickhouse")
    check_clickhouse(clickhouse_client)
    logger.info("Clickhouse is up")

    kafka_client = AdminClient({"bootstrap.servers": KAFKA_SERVERS})
    logger.info("Waiting for Kafka")
    check_kafka(kafka_client)
    logger.info("Kafka is up")


if __name__ == "__main__":
    wait()
