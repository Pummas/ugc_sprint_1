import csv
import datetime
import logging
import random
import uuid

from tqdm import tqdm

from config import (
    BOOKMARKS_COUNT,
    BOOKMARKS_FILENAME,
    DATA_DIR,
    LIKES_COUNT,
    LIKES_FILENAME,
    MOVIES_COUNT,
    MOVIES_FILENAME,
    REVIEWS_COUNT,
    REVIEWS_FILENAME,
    USERS_COUNT,
    USERS_FILENAME,
)
from models import EventBookmark, EventLike, EventReview, Movie, User


def generate_users():
    with open(DATA_DIR / USERS_FILENAME, "w", newline="") as data_file:
        result = []
        fieldnames = ["user_id", "name"]
        writer = csv.DictWriter(data_file, fieldnames=fieldnames, dialect="excel")
        for num in tqdm(range(USERS_COUNT), postfix="users generate"):
            user = User(user_id=uuid.uuid4(), name=f"User {num + 1}")
            writer.writerow(user.dict())
            result.append(user)

        return result


def generate_movies():
    with open(DATA_DIR / MOVIES_FILENAME, "w", newline="") as data_file:
        result = []
        fieldnames = ["movie_id", "name"]
        writer = csv.DictWriter(data_file, fieldnames=fieldnames, dialect="excel")
        for num in tqdm(range(MOVIES_COUNT), postfix="movies generate"):
            movie = Movie(movie_id=uuid.uuid4(), name=f"Movie {num + 1}")
            writer.writerow(movie.dict())
            result.append(movie)

        return result


def generate_bookmarks(users, movies):
    with open(DATA_DIR / BOOKMARKS_FILENAME, "w", newline="") as data_file:
        fieldnames = EventBookmark.__fields__.keys()
        writer = csv.DictWriter(data_file, fieldnames=fieldnames, dialect="excel")
        for num in tqdm(range(BOOKMARKS_COUNT), postfix="bookmarks generate"):
            user = random.choice(users)
            movie = random.choice(movies)
            event = EventBookmark(user_id=user.user_id, movie_id=movie.movie_id)
            writer.writerow(event.dict())


def generate_likes(users, movies):
    like_value = (0, 10)
    with open(DATA_DIR / LIKES_FILENAME, "w", newline="") as data_file:
        fieldnames = EventLike.__fields__.keys()
        writer = csv.DictWriter(data_file, fieldnames=fieldnames, dialect="excel")
        for num in tqdm(range(LIKES_COUNT), postfix="likes generate"):
            user = random.choice(users)
            movie = random.choice(movies)
            like = random.choice(like_value)
            event = EventLike(user_id=user.user_id, movie_id=movie.movie_id, like=like)
            writer.writerow(event.dict())


def generate_reviews(users, movies):
    def gen_text(n: int):
        return f" review comment num {n}"

    with open(DATA_DIR / REVIEWS_FILENAME, "w", newline="") as data_file:
        fieldnames = EventReview.__fields__.keys()
        writer = csv.DictWriter(data_file, fieldnames=fieldnames, dialect="excel")
        for num in tqdm(range(REVIEWS_COUNT), postfix="reviews generate"):
            user = random.choice(users)
            movie = random.choice(movies)
            event = EventReview(
                user_id=user.user_id, movie_id=movie.movie_id, text=gen_text(num), created_at=datetime.datetime.now()
            )
            writer.writerow(event.dict())


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("start data generate")
    users = generate_users()
    movies = generate_movies()
    generate_reviews(users, movies)
    generate_likes(users, movies)
    generate_bookmarks(users, movies)
    logging.info("end data generate")


if __name__ == "__main__":
    main()
