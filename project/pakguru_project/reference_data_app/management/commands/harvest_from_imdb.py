import datetime
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

import datefinder
from imdb import IMDb
from reference_data_app.models import (ShowEpisodeReferenceInfo,
                                       ShowReferenceInfo)


def get_value(d, key):
    try:
        return str(d[key]) if d[key] else ''
    except Exception:
        return ''


def get_date(dt, n):
    if len(dt) == 4:
        date_1 = datetime.datetime.strptime(f'{dt}-01-01', "%Y-%m-%d")
        return date_1 + datetime.timedelta(days=n)
    else:
        matches = datefinder.find_dates(dt)
        date_value = next(iter(matches), False)
        if date_value:
            return date_value.date()
        else:
            return None


def get_movie(movie_id):
    ia = IMDb()
    m = ia.get_movie(movie_id)
    if m:
        return m.items()


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Retrieve show info by Show Info Id.'
        parser.add_argument('id', type=int, help=help_text)

    def handle(self, *args, **options):
        """
        Usage:
        python manage.py harvest_from_imdb 1
        """
        id = options['id']

        print("Argument:")
        print(" id:", id)

        si = ShowReferenceInfo.objects.filter(id=id,
                                              source_type__name='IMDB').first()
        if not si:
            raise CommandError(f'Show Reference ID: {id} not found')
        else:
            print(f'Found show {si.name}')

        movie_id = si.reference_key
        ia = IMDb()
        series = ia.get_movie(movie_id)
        if not series:
            raise CommandError(f'Reference key: {movie_id} not found')

        si.number_of_seasons = series['number of seasons']
        si.cast = {
            'cast': get_value(series, 'cast')
        },
        si.cover_url = series['cover url'],
        si.full_size_cover_url = series['full-size cover url']
        si.extra_data = str(series.items())
        si.save()

        ia.update(series, ['episodes'])
        seasons = sorted(series['episodes'])
        running_number = 1
        for season_number in seasons:
            episodes = series['episodes'][season_number]
            # print(season_number, episodes)
            for episode_number in episodes:
                episode = series['episodes'][season_number][episode_number]
                ei = ShowEpisodeReferenceInfo.objects.filter(show_reference_info=id, season_number=season_number, episode_number=episode_number).first()  # noqa:E501
                if not ei:
                    ei = ShowEpisodeReferenceInfo.objects.create()
                ei.source_type = si.source_type
                ei.show_reference_info = si
                ei.show = si.show
                ei.season_number = season_number
                ei.episode_number = episode_number
                ei.name = episode['long imdb canonical title']
                ei.description = episode['long imdb title']
                ei.year = episode['year']
                ei.running_number = running_number
                ei.original_air_date_from_source = episode['original air date']
                ei.original_air_date = get_date(episode['original air date'], episode_number)  # noqa:E501
                ei.series_title = episode['smart canonical series title']
                ei.episode_title = episode['smart canonical episode title']
                ei.plot = get_value(episode, 'plot')
                ei.extra_data = str(episode.items())
                ei.reference_key = episode.getID()
                ei.added_by = User.objects.get(id=1)
                ei.save()
                running_number += 1
