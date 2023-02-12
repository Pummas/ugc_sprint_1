import time
from typing import Union


def measure_exec_time(cursor, query: str, data: Union[dict, list], insert=False) -> float:
    start = time.time()
    if insert:
        cursor.executemany(query, data, use_prepared_statements=True)
    else:
        cursor.execute(query, data)
    cursor.fetchall()
    return time.time() - start


def calculate_avg(vals: list[float]) -> float:
    return sum(vals) / len(vals)


def select_user_ids(cursor) -> list[str]:
    cursor.execute("""SELECT DISTINCT user_id from test.views""")
    rows = cursor.fetchall()
    return [str(row[0]) for row in rows]


def select_movie_ids(cursor) -> list[str]:
    cursor.execute("""SELECT DISTINCT movie_id from test.views""")
    rows = cursor.fetchall()
    return [str(row[0]) for row in rows]
