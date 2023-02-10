import logging
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError, KafkaTimeoutError
from fastapi import HTTPException

from core.config import settings

producer: AIOKafkaProducer | None = None


async def write_event(topic: str, key: str, value: str):
    try:
        send_future = await producer.send(topic=topic, value=value.encode("utf-8"), key=key.encode("utf-8"))
        response = await send_future  # wait until message is produced

    except KafkaTimeoutError as err:
        logging.error(f"kafka timeout error: {err}")
        raise HTTPException(status_code=HTTPStatus.REQUEST_TIMEOUT, detail="timeout error (Kafka)")

    except KafkaError as err:
        logging.error(f"some kafka error: {err}")
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Error due saving event (Kafka)")

    logging.debug(f"save topic:{topic} key:{key} value:{value}, response:{response}")


async def init_kafka():
    global producer
    kafka = AIOKafkaProducer(client_id=settings.PROJECT_NAME, bootstrap_servers=settings.KAFKA_INSTANCE)
    await kafka.start()
    producer = kafka


async def close_kafka():
    global producer
    if producer:
        await producer.stop()
        producer = None
