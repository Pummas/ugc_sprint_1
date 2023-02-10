import logging

from src.core.constants import FILM_VIEW_TOPIC
from src.core.storage_service import StorageService
from src.db.kafka_producer import write_event
from src.models.dto import DTOViewEvent


class FilmViewStorage(StorageService):
    kafka_topic = FILM_VIEW_TOPIC

    async def save(self, data: DTOViewEvent):
        logging.debug(f"save view: {data.dict()}")
        await write_event(topic=self.kafka_topic, key=str(data.user_id), value=data.json())


# для инъекции зависимостей в FastAPI
def get_film_storage() -> FilmViewStorage:
    return FilmViewStorage()

