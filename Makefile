format:
	black .
	isort .

lint:
	black --check .
	isort --check-only .
	flake8 .
