import uuid
from time import sleep
from typing import List

from model import ViewedFilm

from .utils.mock_etl import MockKafkaConsumer

# количество сообщений для тестирования
MSG_PER_PARTITION = 30
MSG_COUNT = 3 * MSG_PER_PARTITION


def create_test_events(count: int = 10) -> List[ViewedFilm]:
    """Создает тестовый набор данных"""
    result = []
    for i in range(count):
        event = ViewedFilm(user_id=uuid.uuid4(), film_id=uuid.uuid4(), pos_start=i, pos_end=10 * i)
        result.append(event)

    return result


def load_data_to_consumer(consumer: MockKafkaConsumer, data: List[ViewedFilm]) -> None:
    """Загружает данные равномерно по топикам"""
    for i, event in enumerate(data):
        consumer.add_message(message=event.json(), partition=i % len(consumer.topic))


def compare_results(data_in: List[ViewedFilm], data_out: List[dict]) -> bool:
    if not len(data_in) == len(data_out):
        return False
    for event in data_in:
        if not dict(event) in data_out:
            return False

    return True


def test_etl_ok(app_etl):
    etl, clickhouse_db, kafka_consumer = app_etl
    data = create_test_events(count=MSG_COUNT)
    load_data_to_consumer(kafka_consumer, data)

    # надо дать время etl поработать иначе не успевает
    sleep(1)

    assert len(clickhouse_db.data) == MSG_COUNT
    assert compare_results(data, clickhouse_db.data)
    assert kafka_consumer.offsets == [MSG_PER_PARTITION, MSG_PER_PARTITION, MSG_PER_PARTITION]


def test_etl_with_bad_data(app_etl):
    etl, clickhouse_db, kafka_consumer = app_etl

    clickhouse_db.data.clear()
    data = create_test_events(count=MSG_COUNT)
    load_data_to_consumer(kafka_consumer, data)
    kafka_consumer.add_message("bad_string_message_1", partition=0)
    kafka_consumer.add_message("bad_string_message_2", partition=0)
    kafka_consumer.add_message("bad_string_message_3", partition=0)

    # надо дать время etl поработать иначе не успевает
    sleep(1)

    assert len(clickhouse_db.data) == MSG_COUNT
    assert compare_results(data, clickhouse_db.data)
    assert kafka_consumer.offsets == [MSG_PER_PARTITION * 2 + 3, MSG_PER_PARTITION * 2, MSG_PER_PARTITION * 2]
