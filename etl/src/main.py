import clickhouse_driver
import confluent_kafka

import logging_config  # noqa
from config import consumer_config, settings
from etl import ETL
from extractor import KafkaBroker
from loader import Clickhouse
from pre_start import create_kafka_topics
from storage import KafkaStorage
from transformer import KafkaTransformer

if __name__ == "__main__":
    create_kafka_topics(settings.TOPIC_NAMES)

    consumer = confluent_kafka.Consumer(consumer_config)
    consumer.subscribe(settings.TOPIC_NAMES)
    clickhouse_client = clickhouse_driver.Client(host=settings.CLICKHOUSE_HOST)

    broker = KafkaBroker(consumer)
    clickhouse_db = Clickhouse(clickhouse_client)
    transformer = KafkaTransformer()
    storage = KafkaStorage(consumer)

    etl = ETL(extractor=broker, transformer=transformer, loader=clickhouse_db, storage=storage)
    etl.run()
