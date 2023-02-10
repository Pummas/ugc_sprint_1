import clickhouse_driver
import confluent_kafka

from config import consumer_config, settings
from etl import ETL
from extractor import KafkaBroker
from loader import Clickhouse
from pre_start import create_kafka_topics
from storage import KafkaStorage
from transformer import KafkaTransformer

if __name__ == "__main__":
    from _producer import write_events

    create_kafka_topics(settings.TOPIC_NAMES)
    write_events()

    consumer = confluent_kafka.Consumer(consumer_config)
    consumer.subscribe(settings.TOPIC_NAMES)
    clickhouse_client = clickhouse_driver.Client(host=settings.CLICKHOUSE_HOST)

    broker = KafkaBroker(consumer)
    clickhouse_db = Clickhouse(clickhouse_client)
    transformer = KafkaTransformer()
    storage = KafkaStorage(consumer)

    etl = ETL(extractor=broker, transformer=transformer, loader=clickhouse_db, storage=storage)
    etl.run()
