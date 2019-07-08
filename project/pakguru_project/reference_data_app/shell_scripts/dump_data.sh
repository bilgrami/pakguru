#!/bin/bash
app_name=reference_data_app
declare -a models_array
models_array=(ReferenceSourceType ShowReferenceInfo ShowEpisodeReferenceInfo)

for i in "${models_array[@]}"; 
do 
    model_name="$i"
    model_full_name="$app_name.$model_name";
    echo "dumping $model_full_name"; 
    # python manage.py dumpdata reference_data_app.ReferenceSourceType --natural-foreign | python -m json.tool > ./reference_data_app/fixtures/ReferenceSourceType.json
    python manage.py dumpdata $model_full_name --natural-foreign | python -m json.tool > ./$app_name/fixtures/$model_name.json
done
python manage.py encrypt_dump $app_name
