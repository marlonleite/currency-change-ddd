FROM python:3.10-slim-bullseye as base

ENV ENVIRONMENT="not_defined"
ENV TARGET="not_defined"

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV PYTHONHASHSEED=random
ENV POETRY_VERSION=1.1.15

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# System deps:
RUN pip install "poetry==$POETRY_VERSION" --no-cache-dir

# Copy only requirements to cache them in docker layer
WORKDIR /app/

COPY poetry.lock pyproject.toml /app/
COPY alembic.ini /app/
COPY alembic/ /app/alembic/
COPY src/ /app/src/

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
# RUN poetry install --no-interaction --no-ansi --no-dev # prod

COPY entrypoint.sh /tmp/entrypoint.sh

RUN ["chmod", "+x", "/tmp/entrypoint.sh"]
ENTRYPOINT [ "/tmp/entrypoint.sh" ]
