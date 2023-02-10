from abc import abstractmethod

from clickhouse_driver import Client

from model import ViewedFilm


class Database:
    @abstractmethod
    def load(self, *args, **kwargs):
        pass


class Clickhouse(Database):
    def __init__(self, client: Client):
        self.client = client

    def load(self, query: str, data: list[ViewedFilm]):
        try:
            self.client.execute(query, [dict(row) for row in data])
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    def check(self):
        # В дальнейшем выпилить
        print(self.client.execute("SELECT * FROM default.viewed_films "))
