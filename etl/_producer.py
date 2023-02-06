# временный файл, чтобы записать данные в кафку
# для проверки работоспособности
from random import randint
from uuid import uuid4

from confluent_kafka import Producer

from config import producer_config, settings


def random_event() -> (bytes, bytes):
    user_id = uuid4()
    film_id = uuid4()
    seconds = randint(0, 3 * 60 * 60)
    return user_id.bytes + film_id.bytes, seconds.to_bytes(2, "little")


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def write_events():
    producer = Producer(producer_config)
    topic = settings.TOPIC_NAMES[0]
    for i in range(10):
        key, value = random_event()
        producer.produce(topic, key=key, value=value, callback=acked)
        producer.poll()
