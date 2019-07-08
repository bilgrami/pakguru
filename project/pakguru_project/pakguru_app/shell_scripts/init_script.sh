#!/bin/bash

set -e
echo You are running script from $(pwd)
# python manage.py sqlflush  #| python ./manage.py dbshell
# python manage.py makemigrations
python manage.py migrate

echo -----------------------------------------
echo creating superuser [$ADMIN_USER], please wait ..
ADMIN_USER="$ADMIN_USER";
ADMIN_EMAIL="$ADMIN_EMAIL";
ADMIN_PASSWD="$ADMIN_PASSWD";

echo    email=$ADMIN_EMAIL

__script="
from django.contrib.auth.models import User;
if (User.objects.filter(username = '$ADMIN_USER')):
  # User.objects.get(username='$ADMIN_USER', is_superuser=True).delete()
  print ('Warning: Username [$ADMIN_USER] aleady exists. ')
else:
  User.objects.create_superuser('$ADMIN_USER', '$ADMIN_EMAIL', '$ADMIN_PASSWD')

if (User.objects.filter(username = 'shahneela')):
  print ('Warning: Username [shahneela] aleady exists. ')
else:
  User.objects.create_superuser('shahneela', 'shahneela@example.com', 'test123')

"
echo "$__script" | python manage.py shell
echo finished!
echo ----------------------------------------- 

# python manage.py makemigrations
# python manage.py migrate --fake pakguru_app zero
# python manage.py migrate
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
bash $DIR/load_data.sh