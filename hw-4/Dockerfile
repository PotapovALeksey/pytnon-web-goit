FROM python:3.11.7-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false && poetry install --only main

EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
