#!/bin/bash
set -e
echo 'loading data started .. '
# python manage.py sqlflush
python manage.py loaddata Author;
python manage.py loaddata CountryList;
python manage.py loaddata LocaleList;
python manage.py loaddata PostCategoryList;

python manage.py loaddata ShowChannel;
python manage.py loaddata ShowSourceFeed;
python manage.py loaddata Show;
python manage.py loaddata Post;
python manage.py loaddata PostStatistic;

echo 'loading data finished.'
