#!/bin/bash
python manage.py dumpdata pakguru_app.Author > ./pakguru_app/fixtures/Author.json
python manage.py dumpdata pakguru_app.CountryList > ./pakguru_app/fixtures/CountryList.json
python manage.py dumpdata pakguru_app.LocaleList > ./pakguru_app/fixtures/LocaleList.json
python manage.py dumpdata pakguru_app.PostCategoryList > ./pakguru_app/fixtures/PostCategoryList.json
