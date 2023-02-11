format:
	black .
	isort .

lint:
	black --check .
	isort --check-only .
	flake8 .

run:
	docker compose up -d --build

stop:
	docker compose down

etl-logs:
	docker compose logs etl_kafka -f
