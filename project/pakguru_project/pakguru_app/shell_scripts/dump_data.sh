#!/bin/bash
app_name=pakguru_app
declare -a models_array
models_array=(Author CountryList LocaleList PostCategoryList ShowChannel FeedSourceType ShowSourceFeed Show Post PostStatistic ShowFeed_HarvestJobLog)

for i in "${models_array[@]}"; 
do 
    model_name="$i"
    model_full_name="$app_name.$model_name";
    echo "dumping $model_full_name"; 
    # python manage.py dumpdata pakguru_app.Author --natural-foreign | python -m json.tool > ./pakguru_app/fixtures/Author.json
    python manage.py dumpdata $model_full_name --natural-foreign | python -m json.tool > ./$app_name/fixtures/$model_name.json
done
python manage.py encrypt_dump $app_name
