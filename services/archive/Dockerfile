# syntax = docker/dockerfile:1.3
FROM python:3.12-bookworm

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  POETRY_VIRTUAL_ENVS_CREATE=0 \
  POETRY_NO_INTERACTION=1 \
  PIP_DEFAULT_TIMEOUT=10 \
  POETRY_VERSION=1.7.1

RUN pip install --no-cache-dir poetry==$POETRY_VERSION;

COPY poetry.lock* pyproject.toml ./
RUN poetry config installer.max-workers 10
RUN poetry config virtualenvs.create false
RUN export POETRY_REQUESTS_TIMEOUT=100

RUN poetry install -n --no-root

WORKDIR /parser
COPY . /parser

CMD ["bash", "-c", "sleep infinity"]