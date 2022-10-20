.PHONY: test tests install pep8 clean delete proto

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

# Testing
test:
	poetry run pytest --cov=src --color=yes tests/

test_v:
	poetry run pytest --cov=src --color=yes -vv tests/

# Clean up
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .coverage
	rm -rf  coverage_html
	rm -rf .pytest_cache
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	rm -rf celerybeat-schedule
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf __pycache__
	rm -rf */__pycache__
