import logging
from abc import abstractmethod
from typing import List

import backoff
import sentry_sdk
from clickhouse_driver import Client
from clickhouse_driver.errors import Error as ClickhouseError
from clickhouse_driver.errors import NetworkError

from model import ViewedFilm

logger = logging.getLogger(__name__)

CLICKHOUSE_INSERT_QUERY = "INSERT INTO default.viewed_films (user_id, film_id, pos_start, pos_end) VALUES"


class Database:
    @abstractmethod
    def load(self, *args, **kwargs) -> None:
        pass


class Clickhouse(Database):
    def __init__(self, client: Client):
        self.client = client
        self.query = CLICKHOUSE_INSERT_QUERY

    @backoff.on_exception(backoff.expo, exception=NetworkError, logger=logger, max_time=300, max_value=5)
    def load(self, data: List[ViewedFilm]) -> None:
        try:
            self.client.execute(self.query, [dict(row) for row in data])
            logger.debug("Saved %s messages to clickhouse", len(data))
        except ClickhouseError as err:
            logger.exception("Error on loading in clickhouse")
            sentry_sdk.capture_exception(err)
            raise SystemExit("Error on loading in clickhouse")
