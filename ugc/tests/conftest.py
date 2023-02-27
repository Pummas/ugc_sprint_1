import uuid
from typing import List

import pytest
from fastapi.testclient import TestClient

import ugc.tests.source_root  # noqa F401 - прогружает путь до /src/....

# import tests.source_root  # noqa F401 - прогружает путь до /src/....
from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db import film_view_storage
from ugc.src.ugc import app

from .constants import USER_ID


def get_mock_token():
    """test only token"""
    return AccessTokenPayload(
        fresh=False,
        iat=1,
        jti=uuid.uuid4(),
        type="",
        sub=USER_ID,
        nbf=1,
        exp=1,
        name="user",
        roles=["USER"],
        device_id="Android device",
    )


class MockKafka:
    data: List[dict] = []

    async def write_event(self, topic: str, key: str, value: str):
        self.data += [{"topic": topic, "key": key, "value": value}]


@pytest.fixture(scope="module")
def kafka_mock_producer():
    return MockKafka()


@pytest.fixture(scope="module")
def client(kafka_mock_producer):
    app.dependency_overrides[jwt_bearer] = get_mock_token
    test_client = TestClient(app)
    film_view_storage.write_event = kafka_mock_producer.write_event
    return test_client
