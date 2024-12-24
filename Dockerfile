FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY . .

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
