from abc import abstractmethod

from src.core.core_model import CoreModel
from src.core.meta_singleton import MetaSingleton


class StorageService(metaclass=MetaSingleton):
    @abstractmethod
    async def save(self, data: CoreModel):
        """Сохраняет data в хранилище"""
