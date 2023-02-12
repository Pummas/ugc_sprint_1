from abc import abstractmethod
from typing import Any

from confluent_kafka import Consumer, TopicPartition


class Storage:
    @abstractmethod
    def save_offsets(self, offsets: dict[Any, Any]):
        pass

    def get_offsets(self) -> dict[Any, Any]:
        pass


class KafkaStorage(Storage):
    def __init__(self, consumer: Consumer):
        self.consumer = consumer

    def save_offsets(self, offsets: dict[tuple[str, int], int]):
        topic_partitions = [
            TopicPartition(topic=key[0], partition=key[1], offset=value + 1) for key, value in offsets.items()
        ]
        self.consumer.store_offsets(offsets=topic_partitions)

    def get_offsets(self) -> dict[Any, Any]:
        return {}
