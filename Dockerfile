FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python -

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi

COPY . /app

RUN poetry run python manage.py makemigrations
RUN poetry run python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
