import random
from datetime import datetime

from clickhouse_driver import Client

from utils import calculate_avg, measure_exec_time, select_movies_ids_from_db, select_users_ids_from_db

BATCH_SIZES = [1, 10, 200, 500, 1000]
ITERATIONS = 200

INSERT_QUERY = {"insert_rows": """INSERT INTO test.views (id, user_id, movie_id, timestamp, event_time) VALUES"""}


if __name__ == "__main__":
    client = Client(host="localhost")
    users_ids = select_users_ids_from_db(client)
    movies_ids = select_movies_ids_from_db(client)
    with open("insert_test_results.txt", "w") as file:
        for size in BATCH_SIZES:
            results = []
            for _ in range(ITERATIONS):
                values = [
                    {
                        "id": random.randint(0, 100000),
                        "user_id": random.choice(users_ids),
                        "movie_id": random.choice(movies_ids),
                        "timestamp": random.randint(0, 100000),
                        "event_time": datetime.now(),
                    }
                    for _ in range(size)
                ]
                exec_time = measure_exec_time(client, INSERT_QUERY["insert_rows"], values)
                results.append(exec_time)
            avg = calculate_avg(results)
            file.write(f"Query_name: insert_rows, Average_exec_time: {avg}, Count_of_inserted_rows: {size}")
            file.write("\n")
