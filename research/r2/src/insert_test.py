import csv
import datetime
import logging
import time
import uuid

from tqdm import tqdm

from config import BATCHES, RECORD_COUNT, RESULT_DIR
from db import mongo_db, postgres_db

logging.basicConfig(level=logging.INFO)


def data_insert_test(db, count, batch_size=1):
    def get_text(n):
        return f"review text is {n}"

    batch = []
    result = []
    for num in tqdm(range(count), postfix=f" batch={batch_size}"):
        # создаем случайную запись
        data = {
            "film_id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "review_text": get_text(num),
            "created_at": datetime.datetime.now(),
        }

        batch.append(data)

        if len(batch) >= batch_size:
            start = time.time()
            db.test_insert(batch)
            delta = time.time() - start
            result.append([num, delta])
            batch.clear()

    return result


def save_results_to_csv(result: list, file_name):
    with open(RESULT_DIR / file_name, "w", newline="") as data_file:
        field_names = ["id", "time"]
        writer = csv.writer(data_file, dialect="excel")
        writer.writerow(field_names)
        for values in result:
            writer.writerow(values)


def test_loop(db, loop_name=""):
    logging.info(f"insert test for {loop_name}")
    for batch_size in BATCHES:
        results = data_insert_test(db, RECORD_COUNT, batch_size=batch_size)
        save_results_to_csv(results, f"insert_{loop_name}_{batch_size}.csv")


def run_test_mongo():
    db = mongo_db.get_db()
    test_loop(db, loop_name="mongo")
    db.close()


def run_test_postgres():
    db = postgres_db.get_db()
    test_loop(db, loop_name="pg")
    db.close()


def main():
    run_test_mongo()
    run_test_postgres()


if __name__ == "__main__":
    main()
