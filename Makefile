format:
	black .
	isort .

lint:
	black --check .
	isort --check-only .
	flake8 .

make run:
	docker compose up -d --build

make stop:
	docker compose down

etl-logs:
	docker compose logs etl_kafka -f
