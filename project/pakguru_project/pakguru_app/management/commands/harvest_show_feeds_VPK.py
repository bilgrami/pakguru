import datetime
import json
from urllib.parse import urlparse

import dateutil.parser
import django.utils.text
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

import datefinder
# import boto3
import requests
from bs4 import BeautifulSoup
from pakguru_app.models import Post, Show
from pakguru_app.models import ShowFeed_HarvestJobLog as job
from pakguru_app.models import ShowSourceFeed
from reference_data_app.models import ShowEpisodeReferenceInfo as Episode


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Harvest files for active feeds. \n'
        help_text += 'If recreate_all_jobs is true \n'
        help_text += ' Then we expire and recreate all exisiting jobs \n'

        parser.add_argument('recreate_all_jobs', type=str, help=help_text)
        help_text = 'Max number of feeds to process. Use 0 for all'
        parser.add_argument('max_feeds', type=int, help=help_text)

    def handle(self, *args, **options):
        """
        Usage:
        python manage.py harvest_show_feeds_VPK False 0
        python manage.py harvest_show_feeds_VPK True 0
        """
        recreate_all_jobs = options['recreate_all_jobs']
        max_feeds = options['max_feeds']

        print("Arguments:")
        print(" recreate_all_jobs:", recreate_all_jobs)
        print(" max_feeds:", max_feeds)
        FEED_SOURCE_TYPE = 'VPK'
        if recreate_all_jobs == 'True':
            # expire existing feed jobs
            job.objects.filter(is_latest=True, show_feed__feed_source_type__short_code=FEED_SOURCE_TYPE).update(is_active=False, is_latest=False)   # noqa: E128, E501

        feeds = ShowSourceFeed.objects.filter(is_active=True,
                feed_source_type__short_code=FEED_SOURCE_TYPE).all() \
            .exclude(feed_id__in=job.objects.filter(is_active=True)
            .values_list('show_feed_id', flat=True))  # noqa: E128

        feeds = feeds[:max_feeds] if max_feeds > 0 else feeds
        print("Feed count:", len(feeds))

        for feed in feeds:
            feed_url = feed.playlist_link
            # print("feed_url:", feed_url)
            addedby_user = User.objects.get(id=1)
            feed_posts = get_feed_posts(feed_url, feed.show_name)
            feed_data = json.dumps(feed_posts, indent=4)
            # print("feed_data:", feed_data)
            latest_feed = next(iter(feed_posts.items()))
            if latest_feed and not latest_feed[1]['dt']:
                latest_feed_date = datetime.datetime.today().date().isoformat()
            else:
                latest_feed_date = latest_feed[1]['dt']

            # print("latest dt:", latest_feed_date)
            j = job.objects.create(
                show_feed=feed,
                latest_feed_date=latest_feed_date,
                added_by=addedby_user,
                is_latest=True,
                is_active=True
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


def get_domain_from_link(link):
    # if link[:2] == '//':
    #     link = link[2:]
    if 'http' not in link:
        link = 'http:' + link

    return urlparse(link).netloc, link


def extract_links_from_iframe(content):
    links = []
    soup = BeautifulSoup(content, "html.parser")
    for f in soup.find_all('iframe'):
        links.append(f['src'])
    return links


def get_video_from_post(url):
    result = {}
    if url:
        content = str(requests.get(url).content)
        soup = BeautifulSoup(content, "html.parser")
        for f in soup.find_all('iframe'):
            original = f['src']
            host, link = get_domain_from_link(original)
            link = link.replace('embed', 'watch')

            d = {
                'link': link,
                'original': original
            }
            result[host] = d
    return result


def process_lising(listing, show_name):
    a = listing.find('a', href=True)
    link = a['href']
    div_label_text = listing.find('div', class_='archive-list-text')
    label_text = div_label_text.find('h2').get_text()
    episode = -1
    dt = ''
    if "Episode" in label_text:
        if label_text and len(label_text.split(" Episode ")) == 2:
            episode = get_episode(label_text.split(" Episode ")[1])

    dt = get_date(label_text, show_name, episode)
    dt = dt.isoformat()
    return (link, label_text, episode, dt)


def get_episode(str):
    nums = [int(s) for s in str.split() if s.isdigit()]
    return nums[0]


def get_date(label_text, show_name, episode):
    ei = Episode.objects.filter(running_number=episode, show__name='Bulbulay').first()  # noqa: E501
    if ei:
        return ei.original_air_date
    else:
        matches = datefinder.find_dates(label_text)
        dt = next(iter(matches), False)
        if dt:
            dt = dt.date().isoformat()
            return dt + datetime.timedelta(days=episode)


def get_feed_posts(feed_url, show_name):
    page = requests.get(feed_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    mid_container = soup.find('div', {"id": "archive-list-wrap"})
    post_listings = mid_container.find_all('li', class_='infinite-post')
    result = {}

    for listing in post_listings:
        link, label, episode, dt = process_lising(listing, show_name)
        d = {
            'label': label,
            'dt': dt,
            'episode': episode,
            'link': link,
            'video_link': get_video_from_post(link),
        }
        if dt:
            result[str(dt)] = d

    return result
