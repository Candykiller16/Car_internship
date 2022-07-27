FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN pip install pipenv

RUN pipenv install --system --deploy
