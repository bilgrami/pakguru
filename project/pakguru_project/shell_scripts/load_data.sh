#!/bin/bash
set -e
app_name=pakguru_app
declare -a models_array
models_array=(Author CountryList LocaleList PostCategoryList ShowChannel ShowSourceFeed Show Post PostStatistic)

echo 'decrypting data started .. '
python manage.py decrypt_dump
echo 'decrypting data finished'

echo 'loading data started .. '
for i in "${models_array[@]}"; 
do 
    model_name="$i"
    echo "loading $model_name"; 
    # python manage.py loaddata Author;
    python manage.py loaddata $model_name
done
echo 'loading data finished.'

# echo 'removing dump files'
# python manage.py remove_dump
