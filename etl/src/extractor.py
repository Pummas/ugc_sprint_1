from abc import abstractmethod
from typing import Any, Iterator

from confluent_kafka import Consumer, Message


class MessageBroker:
    @abstractmethod
    def extract(self, max_records: int) -> Iterator[Any]:
        pass

    @abstractmethod
    def update_offsets(self, offsets: dict[Any, Any]) -> None:
        pass


class KafkaBroker(MessageBroker):
    def __init__(self, consumer: Consumer):
        self.consumer = consumer

    def extract(self, max_records: int) -> Iterator[Message]:
        for _ in range(max_records):
            msg = self.consumer.poll(1.0)
            if msg is None:
                print("Waiting")
                return
            elif msg.error():
                print(f"ERROR: {msg.error()}")
                return
            else:
                yield msg

    def update_offsets(self, offsets: dict[Any, Any]) -> None:
        pass
