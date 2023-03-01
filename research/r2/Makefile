run_db:
	docker compose -f docker-compose.yml up -d

insert_test:
	python  ./src/insert_test.py

mock_data:
	python ./src/mock_data.py

load_test:
	python  ./src/load_data.py

query_test:
	python  ./src/query_test.py

stop_db:
	docker compose -f docker-compose.yml stop