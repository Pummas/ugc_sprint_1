import json
import uuid
from http import HTTPStatus

from core import auth_bearer

from .constants import USER_ID

FILM_ID = uuid.UUID("4eae4ede-a04c-47d0-bae5-12d5a3433b1f")


def test_ugc_add(client, kafka_mock_producer):
    film_id = FILM_ID
    pos_start = 1
    pos_end = 10
    payload = {"pos_start": pos_start, "pos_end": pos_end}

    response = client.post(f"/ugc/v1/events/movies_view/{film_id}", json=payload)

    assert response.status_code == HTTPStatus.NO_CONTENT

    payload = {"pos_start": pos_end + 1, "pos_end": pos_end + 10}

    response = client.post(f"/ugc/v1/events/movies_view/{film_id}", json=payload)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(kafka_mock_producer.data) == 2

    data = json.loads(kafka_mock_producer.data[0]["value"])
    assert data["user_id"] == str(USER_ID)
    assert data["film_id"] == str(FILM_ID)
    assert data["pos_start"] == 1
    assert data["pos_end"] == 10


def test_ugc_invalid_uuid(client, kafka_mock_producer):
    film_id = "invalid_uuid"
    pos_start = 1
    pos_end = 10
    payload = {"pos_start": pos_start, "pos_end": pos_end}

    response = client.post(f"/ugc/v1/events/movies_view/{film_id}", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_ugc_invalid_payload(client, kafka_mock_producer):
    film_id = FILM_ID
    pos_start = 1
    pos_end = 10
    payload = {"bad_pos_start": pos_start, "pos_end": pos_end}

    response = client.post(f"/ugc/v1/events/movies_view/{film_id}", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_ugc_invalid_token(client, kafka_mock_producer):
    film_id = FILM_ID
    pos_start = 1
    pos_end = 10
    payload = {"pos_start": pos_start, "pos_end": pos_end}

    # убираем мок и вкючаем проверку токена
    auth_bearer.MOCK_TOKEN = False
    client.app.dependency_overrides = {}

    response = client.post(f"/ugc/v1/events/movies_view/{film_id}", json=payload)

    assert response.status_code == HTTPStatus.FORBIDDEN
