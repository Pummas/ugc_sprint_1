import threading

import pytest

import tests.source_root  # noqa F401 - прогружает путь до /src/....
from etl import ETL
from extractor import KafkaBroker
from loader import Clickhouse
from storage import KafkaStorage
from transformer import KafkaTransformer

from .utils.mock_etl import MockClickHouseClient, MockKafkaConsumer


def run_etl_thread(etl: ETL) -> threading.Thread:
    """
    Запускаем ETL в потоке потому что там `while True:`
    """
    thread = threading.Thread(target=etl.run, args=())
    thread.daemon = True
    return thread


@pytest.fixture(scope="module")
def app_etl() -> tuple[ETL, MockClickHouseClient, MockKafkaConsumer]:
    consumer = MockKafkaConsumer(partition_count=3)
    extractor = KafkaBroker(consumer)
    db = MockClickHouseClient()
    transformer = KafkaTransformer()
    loader = Clickhouse(db)
    storage = KafkaStorage(consumer)

    etl_service = ETL(extractor=extractor, transformer=transformer, loader=loader, storage=storage)
    app = run_etl_thread(etl_service)
    app.start()

    return etl_service, db, consumer
