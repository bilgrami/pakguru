#FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7
# pull official base image
FROM ubuntu:latest


RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# set work directory
WORKDIR /app

LABEL Name=pakguru Version=0.0.1

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LISTEN_PORT=5000
EXPOSE 5000

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Tell nginx where static files live (as typically collected using Django's
# collectstatic command.
ENV STATIC_URL /app/static_collected

# Copy the app files to a folder and run it from there
ADD . /app

# Make app folder writable for the sake of db.sqlite3, and make that file also writable.
RUN chmod g+w /app/app/db
RUN chmod g+w /app/app/db/db.sqlite3

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:5000"]