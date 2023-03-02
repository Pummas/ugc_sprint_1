from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session
from models.user_info import Bookmark

router = APIRouter()


@router.post("/{film_id}")
async def create_bookmark(
    film_id,
    db: AsyncIOMotorClient = Depends(get_session),
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    collection = db["bookmarks"]
    user_id = str(token_payload.sub)
    if await collection.find_one({"film_id": film_id, "user_id": user_id}):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Bookmark already exist")
    bookmark = Bookmark(film_id=film_id, user_id=user_id)
    try:
        result = await collection.insert_one(bookmark.dict())
        return {"success": True, "id": str(result.inserted_id)}
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Insert error")


@router.delete("/{film_id}")
async def delete_bookmark(
    film_id: str,
    db: AsyncIOMotorClient = Depends(get_session),
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    collection = db["bookmarks"]
    user_id = str(token_payload.sub)

    try:
        result = await collection.delete_one({"film_id": film_id, "user_id": user_id})
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Delete error")

    if result.deleted_count == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Закладка не найдена")
    return {"deleted": film_id}


@router.get("/", response_model=List[Bookmark])
async def get_bookmarks(
    db: AsyncIOMotorClient = Depends(get_session),
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
):
    collection = db["bookmarks"]
    user_id = str(token_payload.sub)
    try:
        result = collection.find({"user_id": user_id})
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="find error")
    return [Bookmark(**doc) async for doc in result]
