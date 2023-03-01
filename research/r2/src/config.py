from pathlib import Path

BASE_DIR = Path(__file__).parent

PG_CONNECTION_STRING = "postgres://app:123qwe@localhost:5432/test_db"
MONGO_CONNECTION_STRING = "mongodb://localhost:27017"

DATA_DIR = BASE_DIR / "data"
RESULT_DIR = BASE_DIR / "results"

MOVIES_FILENAME = "movies.csv"
USERS_FILENAME = "users.csv"
BOOKMARKS_FILENAME = "bookmarks.csv"
LIKES_FILENAME = "likes.csv"
REVIEWS_FILENAME = "reviews.csv"

LOAD_MONGO_FILENAME = "load_mongo.json"
LOAD_PG_FILENAME = "load_pg.json"

QUERY_MONGO_FILENAME = "query_mongo.json"
QUERY_PG_FILENAME = "query_pg.json"

# --- test 1. insert batches into test base
BATCHES = [1, 2, 5, 10, 20, 40, 80]
RECORD_COUNT = 1_000

# -- mock data config
MOVIES_COUNT = 1_000
USERS_COUNT = 1_000
LIKES_COUNT = 1_000
BOOKMARKS_COUNT = 1_000
REVIEWS_COUNT = 1_000
