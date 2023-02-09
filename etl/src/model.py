from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ViewedFilm(BaseModel):
    user_id: UUID
    film_id: UUID
    film_start_seconds: int
    film_stop_seconds: int
    created_at: datetime
