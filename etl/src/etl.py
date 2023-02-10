from config import settings
from extractor import MessageBroker
from loader import Database
from storage import Storage
from transformer import Transformer

QUERY = "INSERT INTO default.viewed_films (user_id, film_id, film_start_seconds, film_stop_seconds, created_at) VALUES"


class ETL:
    def __init__(self, extractor: MessageBroker, transformer: Transformer, loader: Database, storage: Storage):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.storage = storage
        self.extractor.update_offsets(self.storage.get_offsets())

    def run(self):
        while True:
            data = self.extractor.extract(max_records=settings.MAX_BATCH_SIZE)
            transformed_data = self.transformer.transform(data)
            if transformed_data:
                self.loader.load(QUERY, transformed_data)
                self.storage.save_offsets(self.extractor.last_offsets)
