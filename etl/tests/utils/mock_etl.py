from typing import List

from confluent_kafka.cimpl import TopicPartition


class MockMessage:
    def __init__(self, topic: str, partition: int, offset: int, value: str):
        self._topic = topic
        self._partition = partition
        self._offset = offset
        self._value = value

    def error(self):
        return None

    def topic(self):
        return self._topic

    def partition(self):
        return self._partition

    def offset(self):
        return self._offset

    def value(self):
        return self._value


class MockKafkaConsumer:
    """
    Mock Consumer для тестирования
    можно указывать количество партиций
    но топик только один
    """

    auto_offset = True

    def __init__(self, topic_name: str = "test", partition_count: int = 1):
        self.topic_name = topic_name
        # топик
        self.topic = [[] for _ in range(partition_count)]
        # смещения внутри партиций
        self.offsets = [0] * partition_count

    def poll(self, timeout=None):
        for partition_id, partition in enumerate(self.topic):
            current_offset = self.offsets[partition_id]
            if current_offset < len(partition):
                message = MockMessage(
                    topic=self.topic_name,
                    partition=partition_id,
                    offset=current_offset,
                    value=partition[current_offset],
                )

                if self.auto_offset:
                    self.offsets[partition_id] += 1
                return message

        # если ничего нет
        return None

    def add_message(self, message: str, partition: int = 0):
        """Добавляем событие в партицию"""
        self.topic[partition].append(message)

    def store_offsets(self, offsets: List[TopicPartition]):
        for item in offsets:
            assert self.offsets[item.partition] == item.offset


class MockClickHouseClient:
    """Мок клиент для КликХауса"""

    data: List[dict] = []

    def execute(self, query_str: str, values: List[dict]):
        self.data += values
