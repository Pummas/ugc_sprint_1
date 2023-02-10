from abc import abstractmethod
from typing import Any, Iterator

from model import ViewedFilm


class Transformer:
    @abstractmethod
    def transform(self, data: Iterator[Any]) -> list[Any]:
        pass


class KafkaTransformer(Transformer):
    def transform(self, data: Iterator[bytes]) -> list[ViewedFilm]:
        return [ViewedFilm.parse_raw(record) for record in data]
