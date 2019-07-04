import json
import sys
from datetime import datetime

import dateutil.parser
import django.utils.text
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

# import boto3
import requests
from bs4 import BeautifulSoup
from pakguru_app.models import Post, Show
from pakguru_app.models import ShowFeed_HarvestJobLog as job
from pakguru_app.models import ShowSourceFeed


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Harvest files for active feeds'
        parser.add_argument('feed_id', type=int, help=help_text)

    def handle(self, *args, **options):
        """
        Pseuodo Algrothm:
            find all active feeds belonging to unewstv
            that have no corresponding record in job table

            download feed_posts
                create the new feed job record
                    latest_job.job_status = in-progress
                    latest_job.latest_date = latest_date
                    latest_job.feed_data = feed_posts
                    latest_job.isactive = true

        """
        feed_id = options['feed_id']
        if not feed_id:
            feeds = ShowSourceFeed.objects.filter(is_active=True,
                 feed_source='UNEWSTV').all() \
                .exclude(feed_id__in=job.objects.filter(is_active=True)
                .values_list('show_feed_id', flat=True))  # noqa: E128

            base_url = 'http://www.unewstv.com'
            for feed in feeds:
                feed_url = feed.playlist_link
                addedby_user = User.objects.get(id=1)
                feed_posts = get_feed_posts(base_url, feed_url)
                feed_data = json.dumps(feed_posts, indent=4)
                latest_feed_date = next(iter(feed_posts))
                j = job.objects.create(
                    show_feed=feed,
                    latest_feed_date=latest_feed_date,
                    added_by=addedby_user
                )
                file_name = f'feed_id_{feed.feed_id}-{feed.name}'
                file_name = django.utils.text.slugify(file_name)
                file_name = f'{file_name}.json'
                print("file_name:", file_name)
                j.feed_data.save(file_name, ContentFile(feed_data))
                j.save()
                print(j)

    def get_latest_post(self, show_name, feed_id):
        # show_name = ShowSourceFeed.filter(feed_id=feed_id).show_name
        show = Show.objects.filter(show_name=show_name).first()
        latest_post = Post.objects.filter(show=show).first()
        return latest_post

    def get_latest_feed_posts(self, feed_posts, dt):
        return {k: v for k, v in feed_posts.iteritems()
                if dateutil.parser.parse(k) > dt}


def get_video_from_post(post_url,
                        result_as_json=False):
    if post_url is not None:
        page = requests.get(post_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        f = soup.find('iframe')
        if f is not None:
            embed = f['src']
            link = embed.replace('embed', 'watch')
            if result_as_json:
                d = {
                    'link': link,
                    'embed': embed
                }
                result = {}
                result[post_url] = d
                return result
            else:
                return link
        else:
            return ""


def get_feed_posts(base_url, feed_url):
    page = requests.get(feed_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    post_body = soup.find_all('div', class_='post_body')
    result = {}

    for body in post_body:
        heading = body.find('div', class_='heading')
        a = heading.find('a', href=True)
        link = a['href']
        label = a.get_text()

        la = body.find('div', class_='links_area')
        views = la.find_all('span', class_='partition')[0]
        views = views.find('span', class_='highlight').get_text()
        dt = la.find_all('span', class_='partition')[1]
        dt_label = dt.find('span', class_='highlight').get_text()
        dt = datetime.strptime(dt_label, '%B %d, %Y')
        dt = dt.date().isoformat()

        post_url = base_url + link
        d = {
            'dt_label': dt_label,
            'link': post_url,
            'video_link': get_video_from_post(post_url),
            'label': label,
            'views': views
        }
        result[str(dt)] = d

    return result
