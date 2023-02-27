import uuid
from uuid import UUID
from pydantic import BaseModel, Field


class BaseUserInfo(BaseModel):
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias='_id')
    film_id: str
    user_id: str

    def __init__(self, **data):
        if not data.get('_id'):
            data['_id'] = str(uuid.uuid4())
        super().__init__(**data)


class Like(BaseUserInfo):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {UUID: str}
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "25a660a9-06d7-475d-b1e8-f063d7eb0f28",
                "film_id": "a734abe9-f2b9-4a1a-8f6d-1d3b3f63e3f2",
                "user_id": "fba9e098-57c8-4741-84c7-84f162b133ca"
            }
        }


class Review(BaseUserInfo):
    text: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {UUID: str}
        schema_extra = {
            "example": {
                "id": "25a660a9-06d7-475d-b1e8-f063d7eb0f28",
                "film_id": "a734abe9-f2b9-4a1a-8f6d-1d3b3f63e3f2",
                "user_id": "fba9e098-57c8-4741-84c7-84f162b133ca",
                "text": "Очень интересный фильм, рекомендую посмотреть!"
            }
        }


class Bookmark(BaseUserInfo):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {UUID: str}
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "25a660a9-06d7-475d-b1e8-f063d7eb0f28",
                "film_id": "a734abe9-f2b9-4a1a-8f6d-1d3b3f63e3f2",
                "user_id": "fba9e098-57c8-4741-84c7-84f162b133ca"
            }
        }

