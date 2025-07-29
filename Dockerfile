FROM python:3.12-slim

RUN pip install poetry

WORKDIR /api_project

COPY README.md .

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000"]