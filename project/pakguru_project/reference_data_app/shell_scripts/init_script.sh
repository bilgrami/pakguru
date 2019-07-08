#!/bin/bash

set -e
echo You are running script from $(pwd)
# python manage.py sqlflush  #| python ./manage.py dbshell
# python manage.py makemigrations
python manage.py migrate

# python manage.py makemigrations
# python manage.py migrate --fake pakguru_app zero
# python manage.py migrate
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
bash $DIR/load_data.sh
