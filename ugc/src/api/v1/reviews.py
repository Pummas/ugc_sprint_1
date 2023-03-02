from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session
from models.user_info import Review

router = APIRouter()


@router.post("/{film_id}", response_model=Review)
async def create_review(
    film_id: str,
    text: str,
    token_payload: AccessTokenPayload = Depends(jwt_bearer),
    db: AsyncIOMotorClient = Depends(get_session),
):
    user_id = str(token_payload.sub)
    collection = db["reviews"]
    if await collection.find_one({"film_id": film_id, "user_id": user_id}):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Review already exist")
    review = Review(film_id=film_id, user_id=user_id, text=text)

    try:
        await collection.insert_one(review.dict())
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Insert error")

    return review


@router.get("/", response_model=List[Review])
async def get_reviews(
    film_id: str = None,
    user_id: str = None,
    sort_by: str = "publication_date",
    ascending: bool = False,
    db: AsyncIOMotorClient = Depends(get_session),
):
    collection = db["reviews"]
    query = {}
    if film_id:
        query["film_id"] = film_id
    if user_id:
        query["user_id"] = user_id

    sort_dir = 1 if ascending else -1
    sort_field = sort_by if sort_by in ["publication_date", "id"] else "publication_date"

    try:
        cursor = collection.find(query).sort(sort_field, sort_dir)
    except Exception:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Find error")

    reviews = []
    for doc in await cursor.to_list(length=100):
        reviews.append(Review(**doc))

    return reviews
