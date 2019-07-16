#!/bin/bash
set -e
# True expires and recreates existing jobs
# 0 is to process everything
echo 'running harvest_show_feeds_UNT'
python manage.py harvest_show_feeds_UNT True 0
echo 'running load_harvested_show_feeds'
python manage.py load_harvested_show_feeds -1

echo 'running harvest_show_feeds_DOL'
python manage.py harvest_show_feeds_DOL True 0
echo 'running load_harvested_show_feeds'
python manage.py load_harvested_show_feeds -1

echo 'running harvest_show_feeds_VPK'
python manage.py harvest_show_feeds_VPK True 0
echo 'running load_harvested_show_feeds'
python manage.py load_harvested_show_feeds -1

echo 'running harvest_show_feeds_YT'
python manage.py harvest_show_feeds_YT True 0
echo 'running load_harvested_show_feeds'
python manage.py load_harvested_show_feeds -1

echo 'running clear_cache command '
python manage.py clear_cache

url=https://pak.guru/
curl -s -o /dev/null -w "%{http_code}" $url

url=https://pak.guru/recentshows/
curl -s -o /dev/null -w "%{http_code}" $url

url=https://pak.guru/talkshows/
curl -s -o /dev/null -w "%{http_code}" $url

url=https://pak.guru/comedyshows/
curl -s -o /dev/null -w "%{http_code}" $url

url=https://pak.guru/dramaserials/
curl -s -o /dev/null -w "%{http_code}" $url
