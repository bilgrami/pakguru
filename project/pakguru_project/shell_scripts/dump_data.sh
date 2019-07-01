#!/bin/bash
python manage.py dumpdata pakguru_app.Author | python -m json.tool > ./pakguru_app/fixtures/Author.json
python manage.py dumpdata pakguru_app.CountryList | python -m json.tool > ./pakguru_app/fixtures/CountryList.json
python manage.py dumpdata pakguru_app.LocaleList | python -m json.tool > ./pakguru_app/fixtures/LocaleList.json
python manage.py dumpdata pakguru_app.PostCategoryList | python -m json.tool > ./pakguru_app/fixtures/PostCategoryList.json
python manage.py dumpdata pakguru_app.ShowChannel | python -m json.tool > ./pakguru_app/fixtures/ShowChannel.json
python manage.py dumpdata pakguru_app.ShowSourceFeed | python -m json.tool > ./pakguru_app/fixtures/ShowSourceFeed.json
python manage.py dumpdata pakguru_app.Show | python -m json.tool > ./pakguru_app/fixtures/Show.json
python manage.py dumpdata pakguru_app.Post | python -m json.tool > ./pakguru_app/fixtures/Post.json
python manage.py dumpdata pakguru_app.PostStatistic | python -m json.tool > ./pakguru_app/fixtures/PostStatistic.json
