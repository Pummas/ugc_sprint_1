build:
	docker --log-level=debug build --tag=ugc --target=development -f ./docker/Dockerfile  ./

run:
	sh -c "cd ./src && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

