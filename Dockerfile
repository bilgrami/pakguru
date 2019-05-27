FROM bilgrami/python-base:latest
LABEL Name=pakguru Version=0.0.1 maintainer="Syed Bilgrami <bilgrami@gmail.com>"

# set environment varibles
ENV PROJECT_ROOT /app
# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini
# Tell nginx where static files live (as typically collected using Django's
# collectstatic command.
ENV STATIC_URL /app/static_collected
ENV LISTEN_PORT=5000

WORKDIR $PROJECT_ROOT

EXPOSE 5000

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app files to a folder and run it from there
ADD . $PROJECT_ROOT
# Make app folder writable for the sake of db.sqlite3, and make that file also writable.
RUN chmod g+w $PROJECT_ROOT/app/db/db.sqlite3

CMD python manage.py runserver 0.0.0.0:5000
