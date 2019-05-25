FROM python:3.7-slim

LABEL Name=pakguru Version=0.0.1 maintainer="Syed Bilgrami <bilgrami@gmail.com>"

# set environment varibles
ENV PROJECT_ROOT /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini
# Tell nginx where static files live (as typically collected using Django's
# collectstatic command.
ENV STATIC_URL /app/static_collected
ENV LISTEN_PORT=5000

WORKDIR $PROJECT_ROOT

EXPOSE 5000

# Copy the app files to a folder and run it from there
ADD . /app

# Make app folder writable for the sake of db.sqlite3, and make that file also writable.
RUN chmod g+w /app/app/db/db.sqlite3

RUN \
 apt-get update && \
 apt-get install -y libpq-dev python-dev gcc

RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:5000
