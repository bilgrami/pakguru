#!/bin/bash
# THIS IS THE ROOT FOLDER
declare -a app_name_array
app_name_array=(pakguru_app reference_data_app)

for app_name in "${app_name_array[@]}"; 
do 
    ./$app_name/shell_scripts/init_script.sh
done
