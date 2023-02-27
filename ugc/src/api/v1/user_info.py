import json
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.auth_bearer import AccessTokenPayload, jwt_bearer
from db.user_info_db.database import get_session
from db.user_info_db.models import Bookmark, Like, Review

router = APIRouter()


@router.post("/bookmarks/{film_id}",
             summary="Add bookmark to storage",
             openapi_extra={"x-request-id": "request ID"},
             status_code=HTTPStatus.CREATED,
             )
async def add_bookmark(film_id: str,
                       token_payload: AccessTokenPayload = Depends(jwt_bearer),
                       db: AsyncIOMotorClient = Depends(get_session)
                       ):
    user_id = str(token_payload.sub)
    model = dict(Bookmark(film_id=film_id, user_id=user_id))
    save_response = await db["bookmark"].insert_one(model)
    json_result = json.dumps({'inserted_id': str(save_response.inserted_id)})
    return json_result


@router.post("/likes/{film_id}",
             summary="Add like to storage",
             openapi_extra={"x-request-id": "request ID"},
             status_code=HTTPStatus.CREATED,
             )
async def add_like(film_id: str,
                   token_payload: AccessTokenPayload = Depends(jwt_bearer),
                   db: AsyncIOMotorClient = Depends(get_session)
                   ):
    user_id = str(token_payload.sub)
    model = dict(Like(film_id=film_id, user_id=user_id))
    save_response = await db["likes"].insert_one(model)
    json_result = json.dumps({'inserted_id': save_response.inserted_id})
    return json_result


@router.post("/reviews/{film_id}",
             summary="Add review to storage",
             openapi_extra={"x-request-id": "request ID"},
             status_code=HTTPStatus.CREATED,
             )
async def add_review(film_id: str, text: str,
                     token_payload: AccessTokenPayload = Depends(jwt_bearer),
                     db: AsyncIOMotorClient = Depends(get_session)
                     ):
    user_id = str(token_payload.sub)
    model = dict(Review(film_id=film_id, user_id=user_id, text=text))
    save_response = await db["reviews"].insert_one(model)
    json_result = json.dumps({'inserted_id': str(save_response.inserted_id)})
    return json_result
