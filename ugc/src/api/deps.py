import uuid

from fastapi import Depends

from src.core.auth_bearer import AccessTokenPayload, jwt_bearer
from src.db.film_view_storage import FilmViewStorage

"""Сюда вынесены зависимости чтобы можно было потом при тестах менять"""


def get_film_storage() -> FilmViewStorage:
    return FilmViewStorage()


def get_token(token: AccessTokenPayload = Depends(jwt_bearer)):
    return token


def get_mock_token():
    """test only token. For run without real token"""
    return AccessTokenPayload(
        fresh=False,
        iat=1,
        jti=uuid.uuid4(),
        type="",
        sub=uuid.UUID('044d365d-2884-4fbc-89f3-5ee58d6547d7'),
        nbf=1,
        exp=1,
        name="user",
        roles=["USER"],
        device_id="Android device",
    )
