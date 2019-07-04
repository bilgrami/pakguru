import sys
from datetime import datetime

import dateutil.parser
import django.utils.text
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from pakguru_app.models import Post, Show
from pakguru_app.models import ShowFeed_HarvestJobLog as job


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Process a load feed Job by Job Id. Dupes are ignored'
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
        if job_id == -1:
            jobs = job.objects.filter(is_latest=True, is_active=True).all() \
                    .values_list('job_id', flat=True)  # noqa: E113, E999

            for job.job_id in jobs:
                self.load_show_feed(job.job_id)
        else:
            self.load_show_feed(job_id)

    def load_show_feed(self, job_id):
        latest_job = job.objects.filter(job_id=job_id,
                                        is_latest=True).first()
        if not latest_job:
            raise CommandError(f'Job ID: {job_id} not found')

        feed = latest_job.show_feed
        show = Show.objects.filter(name=feed.show_name).first()
        if not show:
            print(f'Warning: cannot find show: {feed.show_name}, job:{job_id}')
            return
        # find latest_job by feed id
        NS = 'NOT STARTED'
        latest_job_hasnt_started = latest_job and latest_job.job_status == NS
        job_latest_feed_date = latest_job.latest_feed_date
        if latest_job_hasnt_started:
            print("job_latest_feed_date: ", job_latest_feed_date)
            tstart = datetime.now()
            feed_posts = eval(latest_job.feed_data.read())
            print(f"feed_posts retrieved from job: {latest_job.job_id}")
            latest_job.job_status = 'IN PROGRESS'  # in progress
            latest_job.save()
            addedby_user = User.objects.get(id=1)
            tags = [show.host_name, show.name]
            extra_data = {
                "host": show.host_name,
                "job_id": latest_job.job_id,
                "feed_id": feed.feed_id,
                "show_name": show.name,
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

    def get_latest_post(self, show_name, feed_id):
        # show_name = ShowSourceFeed.filter(feed_id=feed_id).show_name
        show = Show.objects.filter(show_name=show_name).first()
        latest_post = Post.objects.filter(show=show).first()
        return latest_post

    def get_latest_feed_posts(self, feed_posts, dt):
        return {k: v for k, v in feed_posts.iteritems()
                if dateutil.parser.parse(k) > dt}
