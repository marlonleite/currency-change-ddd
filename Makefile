.PHONY: test tests install pep8 clean delete proto

DOCKER_COMPOSE_FILE := docker-compose.yml
DOCKER_COMPOSE_DB_CONTAINER_NAME := postgres
API_CONTAINER_NAME := api
PROJECT_NAME := currency_api
DOCKER_COMPOSE := docker-compose -f ${DOCKER_COMPOSE_FILE}

# Poetry and lint
setup:
	poetry install
	poetry run pre-commit install

lint:
	poetry run pre-commit run -a

mypy:
	poetry run mypy src

versions:
	poetry show -l -o

#server
runserver:
	python -m uvicorn src.entrypoints.rest_application:get_app --host 0.0.0.0 --port 8080 --reload

init:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) su -c "python -m alembic init alembic"

makemigrations:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) su -c 'python -m alembic revision --autogenerate -m ""'

migrate:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) su -c "python -m alembic upgrade head"

downgrade:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) su -c "python -m alembic downgrade -1"

up:
	$(DOCKER_COMPOSE) up

stop:
	$(DOCKER_COMPOSE) stop
	$(DOCKER_COMPOSE) ps

down:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) ps

run:
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

build: build_dep run
	@echo "List services"
	$(DOCKER_COMPOSE) ps
	@echo "List docker network"
	docker network ls

build_dep:
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 $(DOCKER_COMPOSE) build --parallel

restart:
	$(DOCKER_COMPOSE) restart $(API_CONTAINER_NAME)

install:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) su -c "poetry install"

env:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) su -c "env"

logs:
	docker logs --follow $(API_CONTAINER_NAME)

bash:
	$(DOCKER_COMPOSE) exec $(API_CONTAINER_NAME) bash

# Testing
test:
	poetry run pytest --cov=src --color=yes tests/

test_v:
	poetry run pytest --cov=src --color=yes -vv tests/

report:
	poetry run pytest --cov=src --color=yes tests/
	coverage report
	coverage html -d htmlcov

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
