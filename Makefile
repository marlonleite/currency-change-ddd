# Poetry and lint
setup:
	cp dev/dev.env .env
	poetry install
	poetry run pre-commit install

lint:
	poetry run pre-commit run -a

mypy:
	poetry run mypy src

init:
	python -m alembic init alembic

makemigrations:
	python -m alembic revision --autogenerate -m ""

migrate:
	python -m alembic upgrade head

downgrade:
	python -m alembic downgrade -1


runserver:
	poetry run python -m uvicorn src.entrypoints.rest_application:get_app --host 0.0.0.0 --port 8080 --reload

cz:
	poetry run cz c
