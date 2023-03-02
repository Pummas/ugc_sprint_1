import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, validator

from core.core_model import CoreModel


class BaseUserInfo(CoreModel):
    film_id: str
    user_id: str


class Like(BaseUserInfo):
    rating: int

    class Config:
        json_encoders = {UUID: str}
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "25a660a9-06d7-475d-b1e8-f063d7eb0f28",
                "film_id": "a734abe9-f2b9-4a1a-8f6d-1d3b3f63e3f2",
                "user_id": "fba9e098-57c8-4741-84c7-84f162b133ca",
            }
        }

    @validator("rating")
    def name_must_contain_space(cls, rating):
        if rating not in [0, 10]:
            raise ValueError("value is not valid")
        return rating


class Review(BaseUserInfo):
    text: str
    published_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        json_encoders = {UUID: str}
        schema_extra = {
            "example": {
                "id": "25a660a9-06d7-475d-b1e8-f063d7eb0f28",
                "film_id": "a734abe9-f2b9-4a1a-8f6d-1d3b3f63e3f2",
                "user_id": "fba9e098-57c8-4741-84c7-84f162b133ca",
                "text": "Очень интересный фильм, рекомендую посмотреть!",
            }
        }


class Bookmark(BaseUserInfo):
    class Config:
        json_encoders = {UUID: str}
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "25a660a9-06d7-475d-b1e8-f063d7eb0f28",
                "film_id": "a734abe9-f2b9-4a1a-8f6d-1d3b3f63e3f2",
                "user_id": "fba9e098-57c8-4741-84c7-84f162b133ca",
            }
        }
