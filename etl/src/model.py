from pydantic import UUID4, BaseModel


class UserFilmView(BaseModel):
    user_id: UUID4
    film_id: UUID4
    seconds: int
