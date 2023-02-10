from abc import abstractmethod
from contextlib import closing
from typing import Iterator

from confluent_kafka import Consumer


class Extractor:
    @abstractmethod
    def fetch(self) -> Iterator[bytes]:
        pass


class KafkaExtractor(Extractor):
    def __init__(self, topics: list[str], config):
        self.consumer = Consumer(config)
        self.consumer.subscribe(topics)

    def fetch(self) -> Iterator[bytes]:
        with closing(self.consumer) as consumer:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                elif msg.error():
                    print(f"ERROR: {msg.error()}")
                else:
                    yield msg.value()
