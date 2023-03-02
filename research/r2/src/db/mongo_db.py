from uuid import UUID

from pymongo import MongoClient

from config import MONGO_CONNECTION_STRING
from models import EventBookmark, EventLike, EventReview, Movie, User

from .base_db import BaseDb


class MongoDB(BaseDb):
    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string, uuidRepresentation="standard")
        self.db = self.client["test_db"]

    def init_db(self):
        collection = self.db["test"]
        collection.drop()

    def clear_test_data(self):
        self.db["person"].drop()
        self.db["movie"].drop()
        self.db["movie"].create_index(
            "likes.person_id", unique=True, partialFilterExpression={"likes.person_id": {"$type": "string"}}
        )
        self.db["movie"].create_index([("likes.person_id", 1), ("likes.score", 1)])

        self.db["movie"].create_index(
            "reviews.person_id", unique=True, partialFilterExpression={"likes.person_id": {"$type": "string"}}
        )

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def test_insert(self, row: list[dict]):
        collection = self.db["test"]
        collection.insert_many(row)

    def _array_update_or_insert(self, collection_name, doc_id, array_name, key_name, value_name, key_value, new_value):
        collection = self.db[collection_name]
        key = {"_id": doc_id, f"{array_name}.{key_name}": {"$ne": key_value}}
        update = {"$push": {array_name: {key_name: key_value, value_name: new_value}}}
        result = collection.update_one(key, update)
        if not result.matched_count:
            key = {"_id": doc_id, f"{array_name}.{key_name}": key_value}
            update = {"$set": {f"{array_name}.$.{value_name}": new_value}}
            result = collection.update_one(key, update)

    def add_bookmark(self, event: EventBookmark):
        key = {"_id": event.user_id}
        update = {"$addToSet": {"bookmarks": event.movie_id}}
        self.db["person"].update_one(key, update)

    def add_like(self, event: EventLike):
        collection = self.db["movie"]
        key = {"_id": event.movie_id, "likes.person_id": {"$ne": event.user_id}}
        update = {"$push": {"likes": {"person_id": event.user_id, "score": event.like}}}
        result = collection.update_one(key, update)
        if not result.matched_count:
            key = {"_id": event.movie_id, "likes.person_id": event.user_id}
            update = {"$set": {"likes.$.score": event.like}}
            result = collection.update_one(key, update)

    def add_review(self, event: EventReview):
        collection = self.db["movie"]
        key = {"_id": event.movie_id, "reviews.person_id": {"$ne": event.user_id}}
        update = {
            "$push": {
                "reviews": {"person_id": event.user_id, "review_text": event.text, "created_at": event.created_at}
            }
        }
        result = collection.update_one(key, update)
        if not result.matched_count:
            key = {"_id": event.movie_id, "reviews.person_id": event.user_id}
            update = {"$set": {"reviews.$.review_text": event.text, "reviews.$.created_at": event.created_at}}
            result = collection.update_one(key, update)

    def add_user(self, user: User):
        self.db["person"].update_one({"_id": user.user_id}, {"$set": {"name": user.name}}, upsert=True)

    def add_movie(self, movie: Movie):
        self.db["movie"].update_one({"_id": movie.movie_id}, {"$set": {"name": movie.name}}, upsert=True)

    def get_user_bookmarks(self, user_id: UUID) -> list[UUID]:
        if query := self.db["person"].find_one({"_id": user_id}, {"bookmarks": 1, "_id": 0}):  # noqa E999
            return query.get("bookmarks", [])
        else:
            return []

    def get_user_likes(self, user_id: UUID) -> list[UUID]:
        """get likes where score is 10 only"""
        # result = self.db['movie'].find({'likes': {'person_id': user_id, 'score': 10}}, {'_id'})
        result = self.db["movie"].find({"likes": {"$elemMatch": {"person_id": user_id, "score": 10}}})
        return [item["_id"] for item in result]

    def get_movie_score(self, movie_id: UUID) -> float:
        result = self.db["movie"].aggregate(
            [{"$match": {"_id": movie_id}}, {"$project": {"_id": 0, "avg_score": {"$avg": "$likes.score"}}}]
        )
        if scores := list(result):  # noqa E999
            return scores[0].get("avg_score", None)
        else:
            return None

    def get_movie_likes(self, movie_id: UUID) -> tuple[int, int]:
        result = self.db["movie"].aggregate(
            [{"$match": {"_id": movie_id}}, {"$unwind": "$likes"}, {"$sortByCount": "$likes.score"}]
        )
        counts = {item["_id"]: item["count"] for item in result}

        # return likes(key=10), dislikes(key=0). may be another?
        return counts.get(10, 0), counts.get(0, 0)


def get_db():
    return MongoDB(connection_string=MONGO_CONNECTION_STRING)
