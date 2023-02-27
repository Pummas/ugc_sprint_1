from uuid import UUID

import psycopg2
from psycopg2.extras import DictCursor

from config import PG_CONNECTION_STRING
from models import EventBookmark, EventLike, EventReview, Movie, User

from .base_db import BaseDb

QUERY_CREATE_TEST_TABLES = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS test;
CREATE TABLE IF NOT EXISTS test (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid,
    film_id uuid,
    review_text TEXT,
    created_at timestamp with time zone
    );
CREATE TABLE IF NOT EXISTS person (
    id uuid PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS movie (
    id uuid PRIMARY KEY,
    name VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS bookmark (
    person_id uuid,
    movie_id uuid
);
CREATE TABLE IF NOT EXISTS movie_like (
    person_id uuid,
    movie_id uuid,
    score smallint
);
CREATE TABLE IF NOT EXISTS review (
    movie_id uuid,
    person_id uuid,
    review_text TEXT,
    created_at timestamptz
);

CREATE UNIQUE INDEX IF NOT EXISTS person_movie_idx ON bookmark(person_id, movie_id);
CREATE UNIQUE INDEX IF NOT EXISTS like_idx ON movie_like(movie_id, person_id);
CREATE UNIQUE INDEX IF NOT EXISTS review_idx ON review(movie_id, person_id);
CREATE INDEX IF NOT EXISTS like_score_idx ON movie_like(person_id, score);
"""
QUERY_INSERT_TEST_DATA = """
INSERT INTO  test(user_id, film_id, review_text, created_at)
VALUES(%(user_id)s, %(film_id)s, %(review_text)s, %(created_at)s);
"""

QUERY_CLEAR_DATA = """
    TRUNCATE TABLE person;
    TRUNCATE TABLE movie;
    TRUNCATE TABLE bookmark;
    TRUNCATE TABLE movie_like;
    TRUNCATE TABLE review;
"""


class PostgresDB(BaseDb):
    def __init__(self, connection_string: str):
        self.connection = psycopg2.connect(connection_string, cursor_factory=DictCursor)
        # self.connection.autocommit = True
        psycopg2.extras.register_uuid()
        self.init_db()

    def init_db(self):
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY_CREATE_TEST_TABLES)
        self.connection.commit()

    def close(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.connection = None

    def test_insert(self, row: list[dict]):
        with self.connection.cursor() as cursor:
            cursor.executemany(QUERY_INSERT_TEST_DATA, row)
        self.connection.commit()

    def add_like(self, event: EventLike):
        QUERY = """
        INSERT INTO movie_like (movie_id, person_id, score)
        VALUES (%(movie_id)s, %(user_id)s, %(like)s)
        ON CONFLICT (movie_id, person_id) DO UPDATE
            SET score = EXCLUDED.score;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY, event.dict())
        self.connection.commit()

    def add_review(self, event: EventReview):
        QUERY = """
        INSERT INTO review (movie_id, person_id, review_text, created_at)
        VALUES (%(movie_id)s, %(user_id)s, %(text)s, %(created_at)s)
        ON CONFLICT (movie_id, person_id) DO UPDATE
            SET review_text = EXCLUDED.review_text,
            created_at = EXCLUDED.created_at;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY, event.dict())
        self.connection.commit()

    def add_user(self, user: User):
        QUERY = """
        INSERT INTO person (id, name) VALUES (%(user_id)s, %(name)s)
        ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY, user.dict())
        self.connection.commit()

    def add_movie(self, movie: Movie):
        QUERY = """
        INSERT INTO movie (id, name) VALUES (%(movie_id)s, %(name)s)
        ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY, movie.dict())
        self.connection.commit()

    def add_bookmark(self, event: EventBookmark):
        QUERY = """
        INSERT INTO bookmark (person_id, movie_id) VALUES (%(user_id)s, %(movie_id)s)
        ON CONFLICT (person_id, movie_id) DO NOTHING;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY, event.dict())
        self.connection.commit()

    def clear_test_data(self):
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY_CLEAR_DATA)
        self.connection.commit()

    def get_user_bookmarks(self, user_id: UUID) -> list[UUID]:
        QUERY = """
        select movie_id from bookmark where person_id='{0}'
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY.format(user_id))
            result = cursor.fetchall()
        return [item[0] for item in result]

    def get_user_likes(self, user_id: UUID) -> list[UUID]:
        QUERY = """
        select movie_id from movie_like where person_id ='{0}' and score=10
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY.format(user_id))
            result = cursor.fetchall()
        return list(map(lambda x: x[0], result))

    def get_movie_score(self, movie_id: UUID) -> float:
        QUERY = """
               select AVG(score) from movie_like where movie_id ='{0}'
                """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY.format(movie_id))
            result = cursor.fetchall()

        return result[0][0]

    def get_movie_likes(self, movie_id: UUID) -> tuple[int, int]:
        QUERY = """
        select score, count(score) from movie_like where movie_id ='{0}'
        group by score
        """
        with self.connection.cursor() as cursor:
            cursor.execute(QUERY.format(movie_id))
            result = cursor.fetchall()
        counts = {item[0]: item[1] for item in result}
        return counts.get(10, 0), counts.get(0, 0)


def get_db():
    return PostgresDB(connection_string=PG_CONNECTION_STRING)
