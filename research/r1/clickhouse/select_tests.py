import random

from clickhouse_driver import Client

from utils import calculate_avg, measure_exec_time, select_movies_ids_from_db, select_users_ids_from_db

ITERATIONS = 200

SELECT_QUERIES = {
    "select_count": """
        SELECT count() FROM test.views
    """,
    "select_max_timestamp_by_user_movie": """
        SELECT MAX (timestamp)
        FROM test.views
        WHERE movie_id = %(movie_id)s
        AND user_id = %(user_id)s
    """,
    "select_max_timestamps_by_user": """
        SELECT movie_id, max(timestamp)
        FROM test.views
        WHERE user_id = %(user_id)s
        GROUP BY movie_id
    """,
    "select_movies_by_user": """
        SELECT DISTINCT (movie_id)
        FROM test.views
        WHERE user_id = %(user_id)s
""",
    "select_users_by_movie": """
        SELECT DISTINCT (user_id) FROM test.views WHERE movie_id = %(movie_id)s
""",
}


if __name__ == "__main__":
    client = Client(host="localhost")
    users_ids = select_users_ids_from_db(client)
    movies_ids = select_movies_ids_from_db(client)
    values = {"user_id": random.choice(users_ids), "movie_id": random.choice(movies_ids)}
    with open("select_test_results.txt", "w") as file:
        for query in SELECT_QUERIES:
            results = []
            for _ in range(ITERATIONS):
                exec_time = measure_exec_time(client, SELECT_QUERIES[query], values)
                results.append(exec_time)
            avg = calculate_avg(results)
            file.write(f"Query_name: {query}, Average_exec_time: {avg}")
            file.write("\n")
