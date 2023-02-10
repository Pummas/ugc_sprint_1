from datetime import datetime
import uuid
from abc import abstractmethod
from uuid import UUID
from model import ViewedFilm

from clickhouse_driver import Client

QUERY = "INSERT INTO default.viewed_films " \
        "(user_id, film_id, film_start_seconds, film_stop_seconds, created_at) VALUES"


class MessageBrocker:
    def __init__(self, client):
        self.client = client

    def extract(self):
        pass


class Database:
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def load(self, *args, **kwargs):
        pass


class Clickhouse(Database):

    def load(self, query, data):
        try:
            self.client.execute(query, [dict(row) for row in data])
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    def check(self):
        # В дальнейшем выпилить
        print(self.client.execute('SELECT * FROM default.viewed_films '))


# TODO: Нужно дописать, пока не используется
class ETL:
    def __init__(self, message_brocker: MessageBrocker, database: Database):
        self.message_brocker = message_brocker
        self.database = database

    def transform(self, data) -> list:
        # Возвращает тестовые данные
        test_data = [
            ViewedFilm(
                user_id=UUID('5c3aaa20-f326-4a95-bd57-e7f7abf2ff6b'),
                film_id=UUID('16d276cf-6697-44fc-87b9-5db334488361'),
                film_start_seconds=0,
                film_stop_seconds=123123123,
                created_at=datetime(2023, 2, 8, 21, 22, 29, 579229)

            ),
            ViewedFilm(
                user_id=UUID('d84689da-c963-4f48-b5c5-4ae4f9569906'),
                film_id=UUID('e5e9a71c-a7be-4c76-a723-162c8b207d94'),
                film_start_seconds=11111,
                film_stop_seconds=999999999,
                created_at=datetime(2023, 9, 8, 21, 22, 29, 579229)

            )
        ]
        return test_data

    def run(self):
        while True:
            data = self.message_brocker.extract()
            tranformed_data = self.transform(data)
            self.database.load(QUERY, tranformed_data)
            return


db_client = Client(host="localhost")

if __name__ == "__main__":
    db_client = Clickhouse(db_client)
    test_message_brocker = MessageBrocker('Пусто')
    etl = ETL(test_message_brocker, db_client)
    etl.run()
    db_client.check()
