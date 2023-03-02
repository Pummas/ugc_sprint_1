from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session
from models.user_info import Like

router = APIRouter()


@router.post(
    "/{film_id}",
    summary="Add like to storage",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.CREATED,
)
async def add_like(
    film_id: str,
    rating: int,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
    db: AsyncIOMotorClient = Depends(get_session),
):
    user_id = str(token_payload.sub)
    if await db["likes"].find_one({"film_id": film_id, "user_id": user_id}):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Like already exist")
    try:
        model = dict(Like(film_id=film_id, user_id=user_id, rating=rating))
    except ValidationError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Error validation")

    try:
        await db["likes"].insert_one(model)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Insert error")

    return "created"


@router.delete(
    "/{film_id}",
    summary="Delete like",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def delete_like(
    film_id: str, token_payload: AccessTokenPayload = Depends(jwt_bearer), db: AsyncIOMotorClient = Depends(get_session)
):
    user_id = str(token_payload.sub)
    collection = db["likes"]

    try:
        result = await collection.delete_one({"film_id": film_id, "user_id": user_id})
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Delete error")

    if result.deleted_count > 0:
        return {"message": "Лайк успешно удален"}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Лайк не найден")


@router.get(
    "/{film_id}",
    summary="get likes and dislikes from film_id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def get_rating(film_id: str, db: AsyncIOMotorClient = Depends(get_session)):
    collection = db["likes"]

    try:
        dislikes = await collection.count_documents({"film_id": film_id, "rating": 0})
        likes = await collection.count_documents({"film_id": film_id, "rating": 10})
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Find error")

    return likes, dislikes


@router.get(
    "/average_rating/{film_id}",
    summary="get average rating from film_id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def get_average_rating(film_id: str, db: AsyncIOMotorClient = Depends(get_session)):
    collection = db["likes"]
    pipeline = [
        {"$match": {"film_id": film_id}},
        {"$group": {"_id": "$film_id", "average_rating": {"$avg": "$rating"}}},
    ]

    try:
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Find error")

    if result:
        return result

    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Not result")


@router.put(
    "/{film_id}",
    summary="update rating from film_id",
    openapi_extra={"x-request-id": "request ID"},
    status_code=HTTPStatus.OK,
)
async def update_like(
    film_id: str,
    rating: int,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
    db: AsyncIOMotorClient = Depends(get_session),
):
    user_id = str(token_payload.sub)
    if rating not in [0, 10]:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Рейтинг должен быть 0 или 10")

    collection = db["likes"]

    try:
        result = await collection.update_one({"film_id": film_id, "user_id": user_id}, {"$set": {"rating": rating}})
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Update error")

    if result.modified_count > 0:
        return {"message": "Лайк успешно обновлен"}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Лайк не найден")
