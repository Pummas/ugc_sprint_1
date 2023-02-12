import random
from datetime import datetime

import vertica_python

from config import CONNECTION_INFO
from utils import calculate_avg, measure_exec_time, select_movie_ids, select_user_ids

BATCH_SIZES = [1, 10, 200, 500, 1000]
ITERATIONS = 200

INSERT_QUERY = """INSERT INTO test.views (user_id, movie_id, timestamp, event_time) VALUES (?, ?, ?, ?)"""


if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_INFO) as connection:
        cursor = connection.cursor()
        user_ids = select_user_ids(cursor)
        movie_ids = select_movie_ids(cursor)
        with open("insert_test_results.txt", "w") as file:
            for size in BATCH_SIZES:
                results = []
                for _ in range(ITERATIONS):
                    values = [
                        (
                            random.choice(user_ids),
                            random.choice(movie_ids),
                            random.randint(0, 100000),
                            datetime.now(),
                        )
                        for _ in range(size)
                    ]
                    result = measure_exec_time(cursor, INSERT_QUERY, values, insert=True)
                    results.append(result)
                avg = calculate_avg(results)
                print(size)
                file.write(f"Query_name: insert_rows, Average_exec_time: {avg}, Count_of_inserted_rows: {size}")
                file.write("\n")
