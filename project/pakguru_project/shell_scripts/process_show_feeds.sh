
#!/bin/bash
set -e
# True expire and recreate all existing jobs
# 0 is to process everything
python manage.py harvest_show_feeds_UNT True 0
python manage.py harvest_show_feeds_DOL True 0
python manage.py harvest_show_feeds_VPK True 0

# load all harvested show feeds
python manage.py load_harvested_show_feeds -1
