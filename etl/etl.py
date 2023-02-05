from clickhouse_driver import Client


class MessageBrocker:
    def __init__(self, client):
        self.client = client

    def extract(self):
        pass


class Database:
    def __init__(self, client):
        self.client = client

    def load(self, data: list):
        pass


class Clickhouse(Database):

    def load(self, data):
        try:

            self.client.execute(
                "INSERT INTO default.viewed_films (user_id, film_id, film_minutes) VALUES",
                ((elem[0], elem[1], elem[2]) for elem in data))
            test = self.client.execute('SELECT * FROM default.viewed_films ')
            print(test)

        except ValueError as e:
            print(e)
            return
        except Exception as e:
            print(e)


db_client = Client(host="localhost")


class ETL:
    def __init__(self, message_brocker: MessageBrocker, database: Database):
        self.message_brocker = message_brocker
        self.database = database

    def transform(self, data) -> list:
        pass

    def run(self):
        while True:
            data = self.message_brocker.extract()
            tranformed_data = self.transform(data)
            self.database.load(tranformed_data)


if __name__ == "__main__":
    client = Clickhouse(db_client)
    test = [(1, 1, 2), (2, 1, 3), (3, 1, 4), (5, 1, 6)]
    client.load(test)
