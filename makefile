fmt:
	poetry run isort src tests
	poetry run black src tests

test:
	poetry run pytest

dev:
	poetry run fastapi dev src/main.py --reload