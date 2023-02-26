import logging
from abc import abstractmethod
from typing import Any, Iterator, List

import sentry_sdk
from pydantic import ValidationError

from model import ViewedFilm

logger = logging.getLogger(__name__)


class Transformer:
    @abstractmethod
    def transform(self, data: Iterator[Any]) -> List[Any]:
        pass


class KafkaTransformer(Transformer):
    def transform(self, data: Iterator[bytes]) -> List[ViewedFilm]:
        result = []
        for record in data:
            try:
                result.append(ViewedFilm.parse_raw(record))
            except ValidationError as err:
                logger.error("Error on creating model ViewedFilm from message %s", record)
                sentry_sdk.capture_exception(err)

        return result
