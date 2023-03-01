import logging

import clickhouse_driver
import confluent_kafka

import logging_config  # noqa
from config import consumer_config, settings
from etl import ETL
from extractor import KafkaBroker
from loader import Clickhouse
from pre_start import create_kafka_topics, init_db
from sentry import init_sentry
from storage import KafkaStorage
from transformer import KafkaTransformer

logger = logging.getLogger(__name__)


init_sentry()

if __name__ == "__main__":
    create_kafka_topics(settings.TOPIC_NAMES)

    consumer = confluent_kafka.Consumer(consumer_config)
    consumer.subscribe(settings.TOPIC_NAMES)
    clickhouse_client = clickhouse_driver.Client(host=settings.CLICKHOUSE_HOST)
    init_db(clickhouse_client)
    broker = KafkaBroker(consumer)
    clickhouse_db = Clickhouse(clickhouse_client)
    transformer = KafkaTransformer()
    storage = KafkaStorage(consumer)

    etl = ETL(extractor=broker, transformer=transformer, loader=clickhouse_db, storage=storage)
    try:
        etl.run()
    except Exception as err:
        # ловим все неожиданные исключения для логирования
        logger.exception(err)
        raise
