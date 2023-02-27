import logging
from typing import List

from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

from config import admin_config

logger = logging.getLogger(__name__)

QUERIES = [
    """
CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER company_cluster;
""",
    """
CREATE TABLE IF NOT EXISTS ugc.viewed_films ON CLUSTER company_cluster
(user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
Engine=ReplicatedMergeTree('/clickhouse/tables/{shard}/viewed_films', '{replica}')
PARTITION BY toYYYYMMDD(created_at) ORDER BY film_id;
""",
    """
CREATE TABLE IF NOT EXISTS default.viewed_films ON CLUSTER company_cluster
(user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
ENGINE = Distributed('company_cluster', ugc, viewed_films, rand());
""",
]


def init_db(db: Client) -> None:
    """Создает таблицы если надо"""
    try:
        for query in QUERIES:
            db.execute(query)
    except Error as err:
        logger.exception("Failed to init ClickHouse db %s", err)
        raise


def create_kafka_topics(topic_names: List[str]) -> None:
    new_topics = [NewTopic(topic_name, num_partitions=6, replication_factor=3) for topic_name in topic_names]
    admin_client = AdminClient(admin_config)
    futures = admin_client.create_topics(new_topics, validate_only=False)

    for topic, future in futures.items():
        try:
            future.result()  # The result itself is None
            logger.info("Topic %s created", topic)
        except KafkaException as err:
            if err.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                logger.info("Topic %s already exist", topic)
            else:
                logger.exception("Failed to create topic %s", topic)
                raise
