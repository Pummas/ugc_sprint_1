import csv
import json
import logging
import time

from tqdm import tqdm

from config import (
    BOOKMARKS_FILENAME,
    DATA_DIR,
    LIKES_FILENAME,
    LOAD_MONGO_FILENAME,
    LOAD_PG_FILENAME,
    MOVIES_FILENAME,
    RESULT_DIR,
    REVIEWS_FILENAME,
    USERS_FILENAME,
)
from db import mongo_db, postgres_db
from models import EventBookmark, EventLike, EventReview, Movie, User


def load_steep(filename, postfix, func):
    with open(filename, newline="") as csv_file:
        count = len(csv_file.readlines())
        csv_file.seek(0)
        reader = csv.reader(csv_file, dialect="excel")
        start = time.time()
        for row in tqdm(reader, postfix=postfix, total=count):
            func(row)
        delta = time.time() - start
    return {"count": count, "time": delta}


def load_loop(db, loop_name=""):
    result = {}
    logging.info(f"load data to {loop_name}")

    test_result = load_steep(
        DATA_DIR / USERS_FILENAME, "load users", lambda row: db.add_user(User(user_id=row[0], name=row[1]))
    )
    result["load users"] = test_result

    test_result = load_steep(
        DATA_DIR / MOVIES_FILENAME, "load movies", lambda row: db.add_movie(Movie(movie_id=row[0], name=row[1]))
    )
    result["load movies"] = test_result

    test_result = load_steep(
        DATA_DIR / BOOKMARKS_FILENAME,
        "load bookmarks",
        lambda row: db.add_bookmark(EventBookmark(user_id=row[0], movie_id=row[1])),
    )
    result["load bookmarks"] = test_result

    test_result = load_steep(
        DATA_DIR / LIKES_FILENAME,
        "load likes",
        lambda row: db.add_like(EventLike(user_id=row[0], movie_id=row[1], like=int(row[2]))),
    )
    result["load likes"] = test_result

    test_result = load_steep(
        DATA_DIR / REVIEWS_FILENAME,
        "load reviews",
        lambda row: db.add_review(EventReview(user_id=row[0], movie_id=row[1], text=row[2], created_at=row[3])),
    )
    result["load reviews"] = test_result

    return result


def save_to_json(result: dict, filename):
    with open(filename, "w") as f:
        json.dump(result, f)


def load_postgres():
    logging.info("pg load")
    db = postgres_db.get_db()
    db.clear_test_data()
    scores = load_loop(db, loop_name="pg")
    save_to_json(scores, RESULT_DIR / LOAD_PG_FILENAME)
    db.close()


def load_mongo():
    logging.info("mongo load")
    db = mongo_db.get_db()
    db.clear_test_data()
    scores = load_loop(db, loop_name="mongo")
    save_to_json(scores, RESULT_DIR / LOAD_MONGO_FILENAME)
    db.close()


def main():
    load_postgres()
    load_mongo()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
