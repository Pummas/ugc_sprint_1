import vertica_python
from research.r1.vertica.config import CONNECTION_INFO

if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_INFO) as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE SCHEMA IF NOT EXISTS test;""")
        cursor.execute(
            """
        CREATE TABLE test.views (
            id IDENTITY,
            user_id UUID NOT NULL,
            movie_id UUID NOT NULL,
            timestamp INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        )
        ORDER BY id;
        """
        )
