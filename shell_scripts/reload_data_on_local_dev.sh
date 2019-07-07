#!/bin/bash
# app_name=pakguru_app
set -e
echo 'Bringing down any running local container'
docker-compose down
echo 'Bringing web container up in detached mode (pointing to production db)'
docker-compose -f docker-compose-hosted-azure-postgres-db.yml up -d
echo 'Running dump script on web container'
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && ./shell_scripts/dump_data.sh'
echo 'Bringing web container down'
docker-compose -f docker-compose-hosted-azure-postgres-db.yml down

echo 'Bringing web container up in detached mode (pointing to dev db)'
docker-compose up -d
echo 'Running any pending migrations'
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && python manage.py migrate'
echo 'Running load script on local container'
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && ./shell_scripts/load_data.sh'
echo 'Bringing local container down'
docker-compose down
echo done
