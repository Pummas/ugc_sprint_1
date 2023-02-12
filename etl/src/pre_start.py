import logging

from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

from config import admin_config

logger = logging.getLogger(__name__)


def create_kafka_topics(topic_names: list[str]) -> None:
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
