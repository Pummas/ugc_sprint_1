from clickhouse_driver import Client

if __name__ == "__main__":
    client = Client(host="localhost")
    client.execute("CREATE DATABASE IF NOT EXISTS test")
    client.execute(
        """
        CREATE TABLE test.views (
            id Int64,
            user_id UUID,
            movie_id UUID,
            timestamp UInt32,
            event_time DateTime
        ) Engine=MergeTree() ORDER BY id
        """
    )
