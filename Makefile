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

build-etl-kafka:
	docker --log-level=debug build  --tag=etl_kafka -f ./etl/docker/Dockerfile   ./etl

build-ugc-service:
	docker --log-level=debug build  --tag=ugc_service --target=production -f ./ugc/docker/Dockerfile   ./ugc

build-all: build-etl-kafka build-ugc-service

prod-run: build-all
	docker compose -f docker-compose.yml up -d