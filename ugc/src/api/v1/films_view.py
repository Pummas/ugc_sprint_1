from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from core.core_model import CoreModel
from db.film_view_storage import FilmViewStorage, get_film_storage
from models.dto import DTOViewEvent


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
    storage: FilmViewStorage = Depends(get_film_storage),
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
) -> Response:
    """
    Add movies_view event to storage. Must be called with JWT access token
     - **film_id**: Film ID (uuid)
    """
    user_id = token_payload.sub
    payload = DTOViewEvent(user_id=user_id, film_id=film_id, pos_start=event.pos_start, pos_end=event.pos_end)
    await storage.save(payload)

    return Response(status_code=HTTPStatus.NO_CONTENT)
