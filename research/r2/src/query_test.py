import csv
import json
import logging
import time
from uuid import UUID

from tqdm import tqdm

from config import DATA_DIR, MOVIES_FILENAME, QUERY_MONGO_FILENAME, QUERY_PG_FILENAME, RESULT_DIR, USERS_FILENAME
from db import mongo_db, postgres_db

users = []
movies = []
user_likes = {}
user_bookmarks = {}
movie_likes = {}
movie_score = {}


def load_data():
    global users
    global movies

    logging.info("load users and movies lists")
    with open(DATA_DIR / USERS_FILENAME, newline="") as csv_file:
        count = len(csv_file.readlines())
        csv_file.seek(0)
        reader = csv.reader(csv_file, dialect="excel")
        users = [UUID(row[0]) for row in tqdm(reader, total=count, postfix="load users")]

    with open(DATA_DIR / MOVIES_FILENAME, newline="") as csv_file:
        count = len(csv_file.readlines())
        csv_file.seek(0)
        reader = csv.reader(csv_file, dialect="excel")
        movies = [UUID(row[0]) for row in tqdm(reader, total=count, postfix="load movies")]


def query_steep(data, postfix, func):
    start = time.time()
    count = len(data)
    for row in tqdm(data, postfix=postfix):
        func(row)
    delta = time.time() - start
    return {"count": count, "time": delta}


def query_loop(db, loop_name):
    result = {}
    logging.info(f"query data from {loop_name}")

    test_result = query_steep(users, "get bookmarks", lambda user_id: db.get_user_bookmarks(user_id))
    result["user get bookmarks"] = test_result

    test_result = query_steep(users, "get likes", lambda user_id: db.get_user_likes(user_id))
    result["user get likes"] = test_result

    test_result = query_steep(movies, "get movie score", lambda movie_id: db.get_movie_score(movie_id))
    result["movie get score"] = test_result

    test_result = query_steep(movies, "get movie likes", lambda movie_id: db.get_movie_likes(movie_id))
    result["movie get likes"] = test_result

    return result


def save_to_json(result: dict, filename):
    with open(filename, "w") as f:
        json.dump(result, f)


def load_postgres():
    db = postgres_db.get_db()
    scores = query_loop(db, loop_name="pg")
    save_to_json(scores, RESULT_DIR / QUERY_PG_FILENAME)
    db.close()


def load_mongo():
    db = mongo_db.get_db()
    scores = query_loop(db, loop_name="mongo")
    save_to_json(scores, RESULT_DIR / QUERY_MONGO_FILENAME)
    db.close()


def eq_test():
    """Тест на эквивалентность значений из двух баз"""
    import math

    dbm = mongo_db.get_db()
    dbp = postgres_db.get_db()
    for user in tqdm(users, postfix="users eq test"):
        res1 = dbm.get_user_bookmarks(user)
        res2 = dbp.get_user_bookmarks(user)
        if set(res1) != set(res2):
            logging.error(f"bookmarks user:{user} {res1}!={res2}")

        res1 = dbm.get_user_likes(user)
        res2 = dbp.get_user_likes(user)
        if set(res1) != set(res2):
            logging.error(f"likes user:{user} {res1}!={res2}")

    for movie in tqdm(movies, postfix="movies eq test"):
        res1 = dbm.get_movie_score(movie)
        res2 = dbp.get_movie_score(movie)
        if res1 is None and res2 is None:
            continue
        if not math.isclose(res1, res2):
            logging.error(f"score movie:{movie} {res1}!={res2}")

        res1 = dbm.get_movie_likes(movie)
        res2 = dbp.get_movie_likes(movie)
        if res1 != res2:
            logging.error(f"likes movie:{movie} {res1}!={res2}")

    dbm.close()
    dbp.close()


def main():
    load_data()
    # можно включить для проверки что функции работают одинаково
    # eq_test()
    load_postgres()
    load_mongo()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
