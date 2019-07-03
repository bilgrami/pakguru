import sys
from datetime import datetime

import dateutil.parser
import django.utils.text
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

import requests
from bs4 import BeautifulSoup
from pakguru_app.models import Post, Show
from pakguru_app.models import ShowFeed_HarvestJobLog as job


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Process a Harbest feed Job by Job Id'
        parser.add_argument('job_id', type=int, help=help_text)

    def handle(self, *args, **options):
        """
        Pseuodo Algrothm:
            find latest_job by feed id
            if latest_job hasnt started:
                feed_posts = from job feed_data
                latest_job.job_status = in-progress
                -- new_posts = all posts for show where target_date
                            does not exists already
                apply feed posts to post model
                latest_job.job_status = finished
            else:
                feed_posts = harvest feed_data from feed_url
                get latest_date from feed_posts
                if latest_date > latest_job.latest_date:
                    new_posts = find all rows that are > latest_job.latest_date
                    in-active previous latest_job.job_status = finished

                    create the new feed job record
                        latest_job.job_status = in-progress
                        latest_job.latest_date = latest_date
                        latest_job.feed_data = feed_posts
                        latest_job.isactive = true
                    apply feed posts to post model
                    latest_job.job_status = finished

        """
        job_id = options['job_id']
        latest_job = job.objects.filter(job_id=job_id,
                                        is_latest=True).first()
        if not latest_job:
            raise CommandError(f'Job ID: {job_id} not found')

        feed = latest_job.show_feed
        show = Show.objects.filter(show_name=feed.show_name).first()
        # find latest_job by feed id
        NS = 'NOT STARTED'
        latest_job_hasnt_started = latest_job and latest_job.job_status == NS
        job_latest_feed_date = latest_job.latest_feed_date
        print("job_latest_feed_date: ", job_latest_feed_date)
        print("latest_job.job_status:", latest_job.job_status)
        if latest_job_hasnt_started:
            tstart = datetime.now()
            feed_posts = eval(latest_job.feed_data.read())
            print(f"feed_posts retrieved from job: {latest_job.job_id}")
            latest_job.job_status = 'IN PROGRESS'  # in progress
            addedby_user = User.objects.get(id=1)
            tags = [show.host_name, show.show_name]
            extra_data = {
                "host": show.host_name,
                "job_id": latest_job.job_id,
                "feed_id": feed.feed_id,
                "show_name": show.show_name,
                "feed_quality": feed.feed_quality
            }
            # self.get_latest_feed_posts(feed_posts, job_latest_feed_date)
            success_count = failed_count = dupes_count = 0
            for k, v in feed_posts.items():
                title = v['label']
                target_date = dateutil.parser.parse(k)
                weekday_name = target_date.strftime("%a").upper()
                slug = django.utils.text.slugify(title)
                post = Post(
                    title=title,
                    slug=slug,
                    target_date=target_date,
                    weekday_name=weekday_name,
                    text=v['video_link'],
                    show=show,
                    is_active=True,
                    is_Show=True,
                    is_Politics=True,
                    tags=tags,
                    extra_data=extra_data,
                    added_by=addedby_user,
                    post_author='Talk Shows Guru',
                    category=show.category,
                    locale=show.locale,
                    media_type='EMBEDDED_VIDEO',
                    source=feed.playlist_link,
                    source_detail=v['link']

                )
                try:
                    post.save()
                    post.country.set(feed.country.all())
                    print(post)
                    success_count += 1

                except IntegrityError:
                    dupes_count += 11
                except Exception:
                    print("Problems?", sys.exc_info())
                    failed_count += 1

            tend = datetime.now()
            duration = str((tend-tstart).total_seconds() * 1000)
            if failed_count == 0:
                latest_job.job_status = 'SUCCESS'
            else:
                latest_job.job_status = 'FAILED'

            extra_data = {
                'ts': str(tstart.isoformat()),
                'te': str(tend.isoformat()),
                'td': duration,
                'S': success_count,
                'F': failed_count,
                'D': dupes_count
            }

            latest_job.extra_data = extra_data
            latest_job.save()
            
        # else:
        #     base_url = 'http://www.unewstv.com'
        #     feed_posts = self.get_feed_posts(base_url, feed.feed_url)

        # # print(json.dumps(feed_posts, indent=4))
        # if feed_posts and 1==0:
        #     dt = list(feed_posts)[0]
        #     latest_feed_date = datetime.strptime(dt, "%Y-%m-%d")
        #     print("latest_feed_date:", latest_feed_date)
        #     print("job_latest_feed_date:", job_latest_feed_date)
        #     if (job_latest_feed_date and
        #        job_latest_feed_date < latest_feed_date and 1 == 0):
        #         # expire existing job logs
        #         q = job.objects.filter(feed_id=feed_id)
        #         q.update(is_latest=False)

        #         # add new job log
        #         job.objects.create(
        #             feed_id=feed_id,
        #             latest_feed_date=latest_feed_date,
        #             is_latest=True
        #         )
        #     # create poosts for each link

    def get_latest_post(self, show_name, feed_id):
        # show_name = ShowSourceFeed.filter(feed_id=feed_id).show_name
        show = Show.objects.filter(show_name=show_name).first()
        latest_post = Post.objects.filter(show=show).first()
        return latest_post

    def get_latest_feed_posts(self, feed_posts, dt):
        return {k: v for k, v in feed_posts.iteritems()
                if dateutil.parser.parse(k) > dt}

    def get_video_from_post(self, post_url,
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

    def get_feed_posts(self, base_url, feed_url):
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
                'video_link': self.get_video_from_post(post_url),
                'label': label,
                'views': views
            }
            result[str(dt)] = d

        return result
