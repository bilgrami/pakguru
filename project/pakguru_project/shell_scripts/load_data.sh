#!/bin/bash
set -e
echo 'loading data started .. '
python manage.py loaddata Author;
python manage.py loaddata CountryList;
python manage.py loaddata LocaleList;
python manage.py loaddata PostCategoryList;
echo 'loading data finished.'
