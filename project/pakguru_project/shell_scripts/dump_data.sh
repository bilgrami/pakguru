#!/bin/bash
python manage.py dumpdata pakguru_app.Author > ./pakguru_app/fixtures/Author.json
python manage.py dumpdata pakguru_app.CountryList > ./pakguru_app/fixtures/CountryList.json
python manage.py dumpdata pakguru_app.LocaleList > ./pakguru_app/fixtures/LocaleList.json
python manage.py dumpdata pakguru_app.PostCategoryList > ./pakguru_app/fixtures/PostCategoryList.json
python manage.py dumpdata pakguru_app.ShowChannel > ./pakguru_app/fixtures/ShowChannel.json
python manage.py dumpdata pakguru_app.ShowSourceFeed > ./pakguru_app/fixtures/ShowSourceFeed.json
python manage.py dumpdata pakguru_app.Show > ./pakguru_app/fixtures/Show.json
python manage.py dumpdata pakguru_app.Post > ./pakguru_app/fixtures/Post.json
python manage.py dumpdata pakguru_app.PostStatistic > ./pakguru_app/fixtures/PostStatistic.json

