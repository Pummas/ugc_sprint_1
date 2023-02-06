from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

from config import admin_config


def create_kafka_topics(topic_names: list[str]) -> None:
    new_topics = [
        NewTopic(topic_name, num_partitions=3, replication_factor=1)
        for topic_name in topic_names
    ]
    admin_client = AdminClient(admin_config)
    futures = admin_client.create_topics(new_topics, validate_only=False)

    for topic, future in futures.items():
        try:
            future.result()  # The result itself is None
            print(f"Topic {topic} created")
        except KafkaException as err:
            if err.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                print(f"Topic {topic} already exist")
            else:
                print(f"Failed to create topic {topic}: {err}")
                raise
