import random
import time
from datetime import datetime
from typing import Optional
from uuid import uuid4

from clickhouse_driver import Client

INSERT_QUERIES = {
    "insert_one_elem_into": """
    INSERT INTO default.test (id, user_id, movie_id, timestamp, event_time) VALUES
    """,
    "insert_many_elems_into": """
    INSERT INTO default.test (id, user_id, movie_id, timestamp, event_time) VALUES
    """,
}

SELECT_QUERIES = {
    "select_count": """
    SELECT count() FROM default.test
    """,
    "select_max_timestamp_by_user_movie": """
        SELECT MAX (timestamp)
        FROM default.test
        WHERE movie_id = 'faa8f831-264d-4326-8517-12cdf5fd249e'
        AND user_id = '86732f54-538d-4a89-91d2-121f311fd75f'
    """,
    "select_max_timestamps_by_user": """
        SELECT movie_id, max(timestamp)
        FROM default.test
        WHERE user_id = '86732f54-538d-4a89-91d2-121f311fd75f'
        GROUP BY movie_id
    """,
    "select_movies_by_user": """
    SELECT DISTINCT (movie_id)
    FROM default.test
    WHERE user_id = '86732f54-538d-4a89-91d2-121f311fd75f'
""",
    "select_users_by_movie": """
    SELECT DISTINCT (user_id) FROM default.test WHERE movie_id = 'faa8f831-264d-4326-8517-12cdf5fd249e'
""",
}
TEST_DATA = {
    "insert_one_elem_into": [
        {
            "id": 1,
            "user_id": "86732f54-538d-4a89-91d2-121f311fd75f",
            "movie_id": "faa8f831-264d-4326-8517-12cdf5fd249e",
            "timestamp": random.randint(0, 100000),
            "event_time": datetime.now(),
        }
    ],
    "insert_many_elems_into": [
        {
            "id": random.randint(0, 100000),
            "user_id": str(uuid4()),
            "movie_id": str(uuid4()),
            "timestamp": random.randint(0, 100000),
            "event_time": datetime.now(),
        }
        for _ in range(1000)
    ],
}


def measure_exec_time(client: Client, query: str, data: Optional[list] = None) -> float:
    start = time.time()
    client.execute(query, data)
    return time.time() - start


if __name__ == "__main__":
    client = Client(host="localhost")
    with open("test_results.txt", "w") as file:
        for query in INSERT_QUERIES:
            exec_time = measure_exec_time(client, INSERT_QUERIES[query], TEST_DATA.get(query))
            file.write(f"Запрос: {query}, Время выполнения: {exec_time}")
            file.write("\n")
        for query in SELECT_QUERIES:
            exec_time = measure_exec_time(client, SELECT_QUERIES[query], TEST_DATA.get(query))
            result = client.execute(SELECT_QUERIES[query])
            file.write(f"Запрос: {query}, Время выполнения: {exec_time}: Результат: {result}")
            file.write("\n")
