FROM python:3.11.5

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install poetry

RUN poetry install --without dev

EXPOSE 5000

ENTRYPOINT ["poetry", "run", "python", "main.py"]