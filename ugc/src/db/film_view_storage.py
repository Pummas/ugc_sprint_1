import logging

from src.core.constants import VIEW_TOPIC
from src.core.storage_service import StorageService, StorageType
from src.db.kafka_producer import write_event
from src.models.dto import DTOViewEvent


class FilmViewStorage(StorageService):
    storage_type = StorageType.FILM_VIEW
    kafka_topic = VIEW_TOPIC

    async def save(self, data: DTOViewEvent):
        logging.debug(f"save view: {data.dict()}")
        await write_event(topic=self.kafka_topic, key=str(data.user_id), value=data.json())
