# временный файл, чтобы записать данные в кафку
# для проверки работоспособности
from datetime import datetime
from random import randint
from uuid import uuid4

from confluent_kafka import Producer

from config import producer_config, settings
from model import ViewedFilm


def random_event() -> ViewedFilm:
    user_id = uuid4()
    film_id = uuid4()
    start = randint(0, 3 * 60 * 60)
    stop = randint(0, 3 * 60 * 60)
    return ViewedFilm(
        user_id=user_id, film_id=film_id, film_start_seconds=start, film_stop_seconds=stop, created_at=datetime.utcnow()
    )


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def write_events():
    producer = Producer(producer_config)
    topic = settings.TOPIC_NAMES[0]
    for i in range(10):
        message_json = random_event().json()
        producer.produce(topic, value=message_json, callback=acked)
        producer.poll()
