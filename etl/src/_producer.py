# временный файл, чтобы записать данные в кафку
# для проверки работоспособности
from random import randint
from uuid import uuid4

from confluent_kafka import Producer

from config import producer_config, settings
from model import UserFilmView


def random_event() -> UserFilmView:
    user_id = uuid4()
    film_id = uuid4()
    seconds = randint(0, 3 * 60 * 60)
    return UserFilmView(user_id=user_id, film_id=film_id, seconds=seconds)


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
