import datetime
import json
from random import randrange

import datefinder
import dateutil.parser
import django.utils.text
# import boto3
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from pakguru_app.models import Post, Show
from pakguru_app.models import ShowFeed_HarvestJobLog as job
from pakguru_app.models import ShowSourceFeed

result = {}


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
        python manage.py harvest_show_feeds_DOL False 0
        python manage.py harvest_show_feeds_DOL True 0

        Pseuodo Algrothm:
            Expire all exisiting jobs if recreate_all_jobs is True

            find all active feeds belonging to DOL
            that have no corresponding record in job table

            download feed_posts
                create the new feed job record
                    latest_job.job_status = in-progress
                    latest_job.latest_date = latest_date
                    latest_job.feed_data = feed_posts
                    latest_job.isactive = true

        """
        recreate_all_jobs = options['recreate_all_jobs']
        max_feeds = options['max_feeds']

        print("Arguments:")
        print(" recreate_all_jobs:", recreate_all_jobs)
        print(" max_feeds:", max_feeds)
        FEED_SOURCE_TYPE = 'DOL'
        if recreate_all_jobs == 'True':
            # expire existing feed jobs
            job.objects.filter(is_latest=True, show_feed__feed_source_type__short_code=FEED_SOURCE_TYPE).update(is_active=False, is_latest=False)   # noqa: E128, E501

        feeds = ShowSourceFeed.objects.filter(is_active=True,
                feed_source_type__short_code=FEED_SOURCE_TYPE).all() \
            .exclude(feed_id__in=job.objects.filter(is_active=True)
            .values_list('show_feed_id', flat=True))  # noqa: E128, E501

        feeds = feeds[:max_feeds] if max_feeds > 0 else feeds
        print("Feed count:", len(feeds))

        for feed in feeds:
            print("feed: id -> ", feed.pk, "-name> ", feed)
            feed_url = feed.playlist_link
            if not feed.extra_data:
                print('Warning: Please check configuration under extra_data')
                continue

            channel = feed.extra_data['channel']
            show_name_from_feed = feed.extra_data['show_name_from_feed']
            additional_feed_url = feed.extra_data['additional_feed_url']
            # print("feed_url:", feed_url)
            # print("channel:", channel)
            # print("additional_feed_url:", additional_feed_url)
            # print("show_name_from_feed:", show_name_from_feed)
            addedby_user = User.objects.get(id=1)
            feed_posts = get_feed_posts(feed_url, additional_feed_url,
                                        channel, show_name_from_feed)
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


def get_video_from_post(post_url):
    if post_url:
        page = requests.get(post_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        f = soup.find('iframe')
        if f:
            embed = f['src']
            return embed.replace('embed', 'watch')
    return ""


def process_lising(listing):
    heading = listing.find('div', class_='list_cont_title')
    a = heading.find('a', href=True)
    link = a['href']
    label_text = a.get_text().replace(' in HD', '')
    category = listing.find('p', class_='list_cont_title').get_text()
    # channel = listing.find('p', class_='list_detail').get_text()
    episode = dt = ''
    in_hd = 'True' if "-in-hd" in link else 'False'
    episode = extract_episode(label_text)
    dt = extract_date(result, label_text, episode)
    return (link, label_text, category, episode, dt, in_hd)


def extract_episode(label_text):
    label = label_text.replace(' in HD', '').replace(' IN hd', '')
    episode = randrange(100) * -1
    if "Episode" in label:
        if label and len(label.split(" Episode ")) >= 2:
            episode = label.split(" Episode ")[-1]

        if label and len(label.split(" Episodee ")) >= 2:
            episode = label.split(" Episodee ")[-1]

    if not type(episode) == int:
        episode = randrange(100) * -1

    return episode


def extract_date(result, label_text, episode):
    matches = datefinder.find_dates(label_text)
    dt = next(iter(matches), False)
    if dt:
        dt = dt.date()
        if dt in result:
            delta = datetime.timedelta(days=episode)
            dt = (dt + delta)
    else:
        dt = datetime.datetime.today()
        delta = datetime.timedelta(days=episode)
        dt = (dt + delta)
        return dt

    if type(dt) == datetime.date:
        dt = dt.isoformat()

    return str(dt)

def get_additional_feed_posts(feed_url, result, channel, show_name):
    pages = [10, 20, 40, 80, 160, 320, 640]
    for pg in pages:
        data = {'var_post': f'{channel}/{show_name}/{pg}'}

        page = requests.post(url=feed_url, data=data)
        soup = BeautifulSoup(page.content, 'html.parser')
        post_listings = soup.find_all('div', class_='list_contents')

        for listing in post_listings:
            link, label, category, episode, dt, in_hd = process_lising(listing)
            d = {
                'label': label,
                'dt': dt,
                'channel': channel,
                'show_name': show_name,
                'episode': episode,
                'category': category,
                'link': link,
                'video_link': get_video_from_post(link),
                'in_hd': in_hd,
                'additional': 'True',
            }

            result[str(dt)] = d

    return result


def get_feed_posts(feed_url, additional_feed_url,
                   channel, show_name_from_feed):
    page = requests.get(feed_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    mid_container = soup.find('div', {"id": "middle-container"})
    post_listings = mid_container.find_all('div', class_='list_contents')

    for listing in post_listings:
        link, label, category, episode, dt, in_hd = process_lising(listing)
        d = {
            'label': label,
            'dt': str(dt),
            'channel': channel,
            'show_name': show_name_from_feed,
            'episode': episode,
            'category': category,
            'link': link,
            'video_link': get_video_from_post(link),
            'in_hd': in_hd,
            'additional': 'False',
        }

        result[str(dt)] = d

    # load more feed_posts
    latest_episode_key = next(iter(result))
    latest_episode = result[latest_episode_key]
    channel = latest_episode['channel']
    show_name = latest_episode['show_name']
    get_additional_feed_posts(additional_feed_url, result, channel, show_name)
    return result
