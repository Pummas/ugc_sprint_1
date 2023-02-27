import random

import vertica_python

from config import CONNECTION_INFO
from utils import calculate_avg, measure_exec_time, select_movie_ids, select_user_ids

ITERATIONS = 200

SELECT_QUERIES = {
    "select_count": """
        SELECT COUNT(*) FROM test.views
    """,
    "select_max_timestamp_by_user_movie": """
        SELECT MAX (timestamp)
        FROM test.views
        WHERE movie_id = :movie_id
        AND user_id = :user_id
    """,
    "select_max_timestamps_by_user": """
        SELECT movie_id, max(timestamp)
        FROM test.views
        WHERE user_id = :user_id
        GROUP BY movie_id
    """,
    "select_movies_by_user": """
        SELECT DISTINCT (movie_id)
        FROM test.views
        WHERE user_id = :user_id
    """,
    "select_users_by_movie": """
        SELECT DISTINCT (user_id) FROM test.views WHERE movie_id = :movie_id
    """,
}

if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_INFO) as connection:
        cursor = connection.cursor()
        user_ids = select_user_ids(cursor)
        movie_ids = select_movie_ids(cursor)
        with open("select_test_results.txt", "w") as file:
            for query in SELECT_QUERIES:
                results = []
                for _ in range(ITERATIONS):
                    data = {
                        "user_id": random.choice(user_ids),
                        "movie_id": random.choice(movie_ids),
                    }
                    result = measure_exec_time(cursor, SELECT_QUERIES[query], data)
                    results.append(result)
                avg = calculate_avg(results)
                file.write(f"Query_name: {query}, Average_exec_time: {avg}")
                file.write("\n")
