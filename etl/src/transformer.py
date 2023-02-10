from abc import abstractmethod
from typing import Any, Iterator

from confluent_kafka import Message

from model import ViewedFilm


class Transformer:
    def __init__(self):
        self.last_offsets = {}

    @abstractmethod
    def transform(self, data: Iterator[Any]) -> Iterator[Any]:
        pass


class KafkaTransformer(Transformer):
    def transform(self, data: Iterator[Message]) -> Iterator[ViewedFilm]:
        self.last_offsets = {}
        for msg in data:
            self.last_offsets[(msg.topic(), msg.partition())] = msg.offset()
            model = ViewedFilm.parse_raw(msg.value())
            print(model)
            print(f"Consumed offset {msg.offset():0>6d} from partition {msg.partition()}")
            yield model
