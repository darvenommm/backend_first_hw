FROM python:3.12.2-alpine3.19

WORKDIR /server

COPY ./pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY . .

CMD [ "sh", "-c", "poetry run alembic upgrade head && poetry run python -u main.py" ]
