import datetime

import django.utils.text
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from pakguru_app.models import ShowFeed_HarvestJobLog as job
from pakguru_app.models import ShowSourceFeed

result = {}


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Harvest files for active YT feeds. \n'
        help_text += 'If recreate_all_jobs is true \n'
        help_text += ' Then we expire and recreate all exisiting jobs \n'

        parser.add_argument('recreate_all_jobs', type=str, help=help_text)
        help_text = 'Max number of feeds to process. Use 0 for all'
        parser.add_argument('max_feeds', type=int, help=help_text)

    def handle(self, *args, **options):
        """
        Usage:
        python manage.py harvest_show_feeds_YT False 0
        python manage.py harvest_show_feeds_YT True 0
        """
        recreate_all_jobs = options['recreate_all_jobs']
        max_feeds = options['max_feeds']

        print("Arguments:")
        print(" recreate_all_jobs:", recreate_all_jobs)
        print(" max_feeds:", max_feeds)
        FEED_SOURCE_TYPE = 'YT'
        if recreate_all_jobs == 'True':
            print('expiring existing feed jobs')
            # job.objects.filter(is_latest=True, show_feed__feed_source_type__short_code=FEED_SOURCE_TYPE).update(is_active=False, is_latest=False)   # noqa: E128, E501
            job.objects.filter(is_latest=True,
            show_feed__feed_source_type__short_code=FEED_SOURCE_TYPE)\
            .exclude(job_status='NOT STARTED')\
            .update(is_active=False, is_latest=False)   # noqa: E128, E501

        feeds = ShowSourceFeed.objects.filter(is_active=True,
                feed_source_type__short_code=FEED_SOURCE_TYPE).all() \
            .exclude(feed_id__in=job.objects.filter(is_active=True)
            .values_list('show_feed_id', flat=True))  # noqa: E128

        feeds = feeds[:max_feeds] if max_feeds > 0 else feeds
        print("Feed count:", len(feeds))

        for feed in feeds:
            print("feed: id -> ", feed.pk, "-name> ", feed)
            feed_url = feed.playlist_link
            addedby_user = User.objects.get(id=1)
            feed_data = get_feed_posts(settings.YT_API_KEY, feed_url, 50)
            latest_feed_date = datetime.datetime.today().date().isoformat()

            # print("latest dt:", latest_feed_date)
            j = job.objects.create(
                show_feed=feed,
                latest_feed_date=latest_feed_date,
                added_by=addedby_user,
                is_latest=True,
                is_active=False
            )
            file_name = f'feed_id_{feed.feed_id}-{feed.name}'
            file_name = django.utils.text.slugify(file_name)
            file_name = f'{file_name}.json'
            print("file_name:", file_name)
            j.feed_data.save(file_name, ContentFile(feed_data))
            j.save()
            print(j.pk, j)


def get_feed_posts(API_KEY, playlist_url, max_results):
    playlist_id = playlist_url.split('&list=')[-1]    
    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2Cid&maxResults={max_results}&playlistId={playlist_id}&fields=etag%2CeventId%2Citems%2Ckind%2CnextPageToken%2CpageInfo%2CprevPageToken%2CtokenPagination%2CvisitorId&key={API_KEY}'

    result = requests.get(url).content
    data = result.decode('utf8').replace("'", '"')
    return data
