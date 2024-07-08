
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

WORKDIR /django_app

COPY ./Messenger/django_app/Messenger/

RUN pip install --no-cache-dir -r /django_app/Messenger/requirements.txt

WORKDIR /django_app/Messenger

COPY . .

RUN python manage.py migrate

EXPOSE 8000
