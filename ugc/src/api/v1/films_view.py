from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from src.api.deps import get_film_storage, get_token  # get_mock_token - for test
from src.core.auth_bearer import AccessTokenPayload
from src.core.core_model import CoreModel
from src.core.storage_service import StorageService
from src.models.dto import DTOViewEvent


class ViewEvent(CoreModel):
    pos_start: int  # начало просмотра фильма, время в секундах с начала фильма
    pos_end: int  # конец просмотра фильма, время в секундах с начала фильма


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.post(
    "/movies_view/{film_id}",
    summary="Add movies_view event to storage",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.NO_CONTENT,
)
async def add_movie_view(
    film_id: UUID,
    event: ViewEvent,
    storage: StorageService = Depends(get_film_storage),
    token_payload: AccessTokenPayload = Depends(get_token),  # get_mock_token - for test
):
    """
    Add movies_view event to storage. Must be called with JWT access token
     - **film_id**: Film ID (uuid)
    """
    user_id = token_payload.sub
    payload = DTOViewEvent(user_id=user_id, film_id=film_id, pos_start=event.pos_start, pos_end=event.pos_end)
    await storage.save(payload)

    return Response(status_code=HTTPStatus.NO_CONTENT)
