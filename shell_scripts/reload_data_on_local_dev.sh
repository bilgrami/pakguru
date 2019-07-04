#!/bin/bash
# app_name=pakguru_app
set -e
echo Bringing production container up in detached mode
docker-compose -f docker-compose-hosted-azure-postgres-db.yml up -d
echo Running dump script on production container
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && ./shell_scripts/dump_data.sh'
echo Bringing production container down
docker-compose -f docker-compose-hosted-azure-postgres-db.yml down

echo Bringing local container up in detached mode
docker-compose up -d
echo Running load script on production container
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && ./shell_scripts/load_data.sh'
echo Bringing local container down
docker-compose down
