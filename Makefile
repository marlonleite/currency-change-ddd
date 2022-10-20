# Poetry and lint
setup:
	cp dev/dev.env .env
	poetry install
	poetry run pre-commit install

lint:
	poetry run pre-commit run -a

mypy:
	poetry run mypy src

runserver:
	poetry run python -m uvicorn src.entrypoints.rest_application:get_app --host 0.0.0.0 --port 8080 --reload

commit:
	poetry run cz c
