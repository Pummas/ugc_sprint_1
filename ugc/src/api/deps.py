import uuid

from fastapi import Depends

from src.core.auth_bearer import AccessTokenPayload, jwt_bearer
from src.core.storage_service import StorageService, StorageType
from src.db.film_view_storage import FilmViewStorage

"""Сюда вынесены зависимости чтобы можно было потом при тестах менять"""


def get_film_storage() -> StorageService:
    storage: FilmViewStorage = StorageService.get_storage(StorageType.FILM_VIEW)
    return storage


def get_token(token=Depends(jwt_bearer)):
    return token


def get_mock_token():
    """test only token"""
    return AccessTokenPayload(
        fresh=False,
        iat=1,
        jti=uuid.uuid4(),
        type="",
        sub=uuid.uuid4(),
        nbf=1,
        exp=1,
        name="user",
        roles=["USER"],
        device_id="Android device",
    )
