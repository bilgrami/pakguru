#!/bin/bash
set -e
# True expire and recreate all existing jobs
# 0 is to process everything
echo 'running harvest_show_feeds_UNT'
python manage.py harvest_show_feeds_UNT True 0
echo 'running harvest_show_feeds_DOL'
python manage.py harvest_show_feeds_DOL True 0
echo 'running harvest_show_feeds_VPK'
python manage.py harvest_show_feeds_VPK True 0

echo 'running load_harvested_show_feeds'
python manage.py load_harvested_show_feeds -1
