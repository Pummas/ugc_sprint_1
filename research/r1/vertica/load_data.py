import logging
import random
from datetime import datetime
from uuid import uuid4

import vertica_python
from research.r1.vertica.config import CONNECTION_INFO

logger = logging.getLogger(__name__)

BATCH_SIZE = 1000
USER_NUMBER = 10000
MOVIES_NUMBER = 10000
BATCH_NUMBER = 10000

QUERY = """INSERT INTO test.views (user_id, movie_id, timestamp, event_time) VALUES (?, ?, ?, ?)"""

user_ids = [str(uuid4()) for _ in range(USER_NUMBER)]
movie_ids = [str(uuid4()) for _ in range(MOVIES_NUMBER)]


def generate_and_load_data(cursor):
    for i in range(BATCH_NUMBER):
        values = [
            (
                random.choice(user_ids),
                random.choice(movie_ids),
                random.randint(0, 100000),
                datetime.now(),
            )
            for _ in range(BATCH_SIZE)
        ]
        try:
            cursor.executemany(QUERY, values, use_prepared_statements=True)
        except Exception as error:
            logger.error(f"Error loading data: {error}")


if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_INFO) as connection:
        cursor = connection.cursor()
        generate_and_load_data(cursor)
