include .env

up/db:
	@echo "Starting databases"
	@docker-compose up -d db cache

up/all:
	@echo "Starting all services"
	@docker-compose up -d

load_env:
	@echo "Loading environment variables from .env file"
	@export $(shell sed 's/=.*//' .env)

fmt:
	poetry run isort src tests
	poetry run black src tests

test:
	poetry run pytest

cov:
	poetry run pytest --cov=src --cov-report=term-missing

dev: load_env up/db
	poetry run fastapi dev src/main.py --reload

start: load_env up/all
	poetry run fastapi run src/main.py --reload