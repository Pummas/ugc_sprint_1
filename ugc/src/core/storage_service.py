from abc import ABC, abstractmethod
from enum import Enum

from src.core.core_model import CoreModel


class StorageType(Enum):
    MOCK = 0
    FILM_VIEW = 1


class StorageService(ABC):
    storages = {}
    storage_type: StorageType

    @abstractmethod
    async def save(self, data: CoreModel):
        """Сохраняет data в хранилище"""

    @classmethod
    def get_storage(cls, storage_type: StorageType) -> "StorageService":
        storage = cls.storages.get(storage_type)
        if storage:
            return storage

        for storage_cls in cls.__subclasses__():
            if storage_cls.storage_type == storage_type:
                storage = storage_cls()
                cls.storages[storage_type] = storage
                return storage

        raise ValueError(f" Storage with type:{storage_type.name} not found")
