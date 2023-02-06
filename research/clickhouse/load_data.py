import logging
import random
from datetime import datetime
from uuid import uuid4

from clickhouse_driver import Client
from clickhouse_driver.errors import Error

logger = logging.getLogger(__name__)

client = Client(host="localhost")

BATCH_SIZE = 1000
USER_NUMBER = 10000
MOVIES_NUMBER = 10000
BATCH_NUMBER = 10000

QUERY = """INSERT INTO default.test (id, user_id, movie_id, timestamp, event_time) VALUES"""


def generate_and_load_data():
    for i in range(BATCH_NUMBER):
        values = [
            {
                "id": random.randint(0, 100000),
                "user_id": str(uuid4()),
                "movie_id": str(uuid4()),
                "timestamp": random.randint(0, 100000),
                "event_time": datetime.now(),
            }
            for _ in range(BATCH_SIZE)
        ]
        try:
            client.execute(QUERY, values)
        except Error as error:
            logger.error(f"Error loading data: {error}")


if __name__ == "__main__":
    generate_and_load_data()
