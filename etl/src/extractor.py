import logging
from abc import abstractmethod
from typing import Any, Dict, Iterator

from confluent_kafka import Consumer

logger = logging.getLogger(__name__)


class MessageBroker:
    def __init__(self):
        self.last_offsets = {}

    @abstractmethod
    def extract(self, max_records: int) -> Iterator[Any]:
        pass

    @abstractmethod
    def update_offsets(self, offsets: Dict[Any, Any]) -> None:
        pass


class KafkaBroker(MessageBroker):
    def __init__(self, consumer: Consumer):
        super().__init__()
        self.consumer = consumer

    def extract(self, max_records: int) -> Iterator[bytes]:
        self.last_offsets = {}
        for _ in range(max_records):
            msg = self.consumer.poll(1.0)
            if msg is None:
                logger.debug("Waiting for messages")
                return
            elif msg.error():
                logger.error("ERROR: %s", msg.error())
                return
            else:
                self.last_offsets[(msg.topic(), msg.partition())] = msg.offset()
                logger.debug("Consumed %s", msg.value())
                yield msg.value()
        logger.debug("Offsets in batch %s", self.last_offsets)

    def update_offsets(self, offsets: Dict[Any, Any]) -> None:
        # оффсеты автоматически берутся из кафки, поэтому не нужно из обновлять
        pass
