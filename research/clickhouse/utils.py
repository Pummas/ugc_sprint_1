import time
from typing import Union

from clickhouse_driver import Client


def measure_exec_time(client: Client, query: str, data: Union[dict, list]) -> float:
    start = time.time()
    client.execute(query, data)
    return time.time() - start


def calculate_avg(vals: list[float]) -> float:
    return sum(vals) / len(vals)


def select_users_ids_from_db(client: Client) -> list:
    users_ids = [str(row[0]) for row in client.execute("""SELECT DISTINCT user_id from test.views""")]
    return users_ids


def select_movies_ids_from_db(client: Client) -> list:
    movies_ids = [str(row[0]) for row in client.execute("""SELECT DISTINCT movie_id from test.views""")]
    return movies_ids
