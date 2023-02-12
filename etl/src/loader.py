import logging
from abc import abstractmethod

from clickhouse_driver import Client

from model import ViewedFilm

logger = logging.getLogger(__name__)

CLICKHOUSE_INSERT_QUERY = (
    "INSERT INTO default.viewed_films (user_id, film_id, film_start_seconds, film_stop_seconds, created_at) VALUES"
)


class Database:
    @abstractmethod
    def load(self, *args, **kwargs) -> None:
        pass


class Clickhouse(Database):
    def __init__(self, client: Client):
        self.client = client
        self.query = CLICKHOUSE_INSERT_QUERY

    def load(self, data: list[ViewedFilm]) -> None:
        try:
            self.client.execute(self.query, [dict(row) for row in data])
            logger.debug("Saved %s messages to clickhouse", len(data))
        except ValueError:
            logger.exception("Value error on loading in clickhouse")
            raise
        except Exception:
            logger.exception("Error on loading in clickhouse")
            raise
