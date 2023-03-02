import datetime
from uuid import UUID

from core_model import CoreModel


class User(CoreModel):
    user_id: UUID
    name: str


class Movie(CoreModel):
    movie_id: UUID
    name: str


class MovieBookmarks(CoreModel):
    user: User
    movies: list[Movie]


class UserLike(CoreModel):
    user: User
    like: int


class MovieLikes(CoreModel):
    movie: Movie
    likes: list[UserLike]


class UserReview(CoreModel):
    user: User
    timestamp: datetime.datetime
    text: str
    likes: list[UserLike] | None


class MovieReviews(CoreModel):
    movie: Movie
    reviews: list[UserReview]


class ExUser(User):
    bookmarks: list[Movie]


class ExMovie(Movie):
    reviews: list[UserReview]


# ------------------------------------------------------------------------------ #


# Классы ниже описывают предпологаемые события от пользователя
class EventBookmark(CoreModel):
    """Закладка на фильм"""

    user_id: UUID
    movie_id: UUID


class EventLike(CoreModel):
    """Лайк на фильм"""

    user_id: UUID
    movie_id: UUID
    like: int


class EventReview(EventBookmark):
    """Комментарий на фильм"""

    user_id: UUID
    movie_id: UUID
    text: str
    created_at: datetime.datetime


class EventReviewLike(EventLike):
    """Лайк на обзор - или у обзора будет свой id?"""

    user_id: UUID
    movie_id: UUID
    like: int
