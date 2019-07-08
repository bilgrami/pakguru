#!/bin/bash
set -e
app_name=reference_data_app
declare -a models_array
models_array=(ReferenceSourceType ShowReferenceInfo ShowEpisodeReferenceInfo)

echo 'decrypting data started .. '
python manage.py decrypt_dump $app_name
echo 'decrypting data finished'

echo 'loading data started .. '
for i in "${models_array[@]}"; 
do 
    model_name="$i"
    echo "loading $model_name"; 
    # python manage.py loaddata Author;
    python manage.py loaddata --app $app_name $model_name
done
echo 'loading data finished.'

# echo 'removing dump files'
# python manage.py remove_dump $app_name
