from abc import ABC, abstractmethod
from uuid import UUID

from models import EventBookmark, EventLike, EventReview, Movie, User


class BaseDb(ABC):
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def test_insert(self, row: list[dict]):
        pass

    @abstractmethod
    def add_bookmark(self, event: EventBookmark):
        pass

    @abstractmethod
    def add_like(self, event: EventLike):
        pass

    @abstractmethod
    def add_review(self, event: EventReview):
        pass

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def add_movie(self, movie: Movie):
        pass

    @abstractmethod
    def clear_test_data(self):
        pass

    @abstractmethod
    def get_user_bookmarks(self, user_id: UUID) -> list[UUID]:
        pass

    @abstractmethod
    def get_user_likes(self, user_id: UUID) -> list[UUID]:
        pass

    @abstractmethod
    def get_movie_score(self, movie_id: UUID) -> float:
        pass

    @abstractmethod
    def get_movie_likes(self, movie_id: UUID) -> tuple[int, int]:
        pass
