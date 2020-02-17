import sys
from datetime import datetime

import dateutil.parser
import django.utils.text
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

import datefinder
from pakguru_app.models import Post, Show
from pakguru_app.models import ShowFeed_HarvestJobLog as job
from django.db.models import Max


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Process a load feed Job by Job Id. Dupes are ignored'
        parser.add_argument('job_id', type=int, help=help_text)

    def handle(self, *args, **options):
        job_id = options['job_id']
        if job_id == -1:  # process all jobs
            jobs = job.objects.filter(is_latest=True, is_active=True).all() \
                    .values_list('job_id', flat=True)  # noqa: E113, E999

            for job.job_id in jobs:
                self.load_show_feed(job.job_id)
        else:
            self.load_show_feed(job_id)

    def get_flag(self, data, flag_name):
        if data and flag_name in data:
            return True if data[flag_name] == 1 else False
        return False

    def load_show_feed(self, job_id):
        print("Processing Job Id:", job_id)
        latest_job = job.objects.filter(job_id=job_id,
                                        is_latest=True).first()
        if not latest_job:
            raise CommandError(f'Job ID: {job_id} not found')

        feed = latest_job.show_feed
        show = Show.objects.filter(name=feed.show_name).first()
        if not show:
            failure_message = (f'Warning: Unknown show: {feed.show_name}, '
                               f'job:{job_id}')
            extra_data = {
                'job_id': job_id,
                'error': failure_message,
                'feed_id': feed.feed_id,
                'previous_extra_data': latest_job.extra_data
            }
            latest_job.extra_data = extra_data
            latest_job.save()
            print(failure_message)
            return
        # find latest_job by feed id
        NS = 'NOT STARTED'
        latest_job_hasnt_started = latest_job and latest_job.job_status == NS
        job_latest_feed_date = latest_job.latest_feed_date
        if latest_job_hasnt_started:
            print("job_latest_feed_date: ", job_latest_feed_date)
            tstart = datetime.now()
            feed_posts = {}
            if latest_job.feed_data:
                try:
                    feed_posts = eval(latest_job.feed_data.read())
                    print(f"feed_posts retrieved from job: {latest_job.job_id}")
                except Exception:
                    print('error reading feed file')
                    return

            latest_job.job_status = 'IN PROGRESS'  # in progress
            latest_job.save()
            addedby_user = User.objects.get(id=1)
            tags = [show.host_name, show.name]
            extra_data = {
                "host": show.host_name,
                "job_id": latest_job.job_id,
                "feed_id": feed.feed_id,
                "feed_name": feed.name,
                "show_name": show.name,
                "feed_quality": feed.feed_quality
            }
            # self.get_latest_feed_posts(feed_posts, job_latest_feed_date)
            success_count = failed_count = dupes_count = 0
            for k, v in feed_posts.items():
                failure_message = ''
                episode = -1
                title = v['label']
                if not k:
                    print("Empty key found for title. skipping..", title, v)
                    continue

                slug = django.utils.text.slugify(title)
                video_link = v['video_link']
                show_posts = Post.objects.filter(show__show_id=show.show_id).all()  # noqa:E501
                total_shows = len(show_posts) + 1

                if 'episode' in v:
                    episode = int(v['episode'])
                else:
                    episode_dict = show_posts.aggregate(Max('episode_number'))
                    episode = episode_dict['episode_number__max'] + 1
                is_show = is_politics = True
                is_joke = is_quote = False
                extra_data['feed_post'] = v
                if show.extra_data:
                    is_show = self.get_flag(show.extra_data, 'is_Show')
                    is_politics = self.get_flag(show.extra_data, 'is_Politics')
                    is_joke = self.get_flag(show.extra_data, 'is_Joke')
                    is_quote = self.get_flag(show.extra_data, 'is_Quote')

                matches = datefinder.find_dates(k)
                target_date = next(iter(matches), False)
                if target_date:
                    target_date = target_date.date()
                    weekday_name = target_date.strftime("%a").upper()

                post = Post.objects.filter(slug=slug).first()
                if not post:
                    # create new post
                    post = Post(
                        title=title,
                        name=title,
                        slug=slug,
                        target_date=target_date,
                        weekday_name=weekday_name,
                        text=video_link,
                        show=show,
                        is_active=True,
                        is_Show=is_show,
                        is_Politics=is_politics,
                        is_Joke=is_joke,
                        is_Quote=is_quote,
                        tags=tags,
                        extra_data=extra_data,
                        added_by=addedby_user,
                        post_author='Talk Shows Guru',
                        category=show.category,
                        locale=show.locale,
                        media_type='EMBEDDED_VIDEO',
                        source=feed.playlist_link,
                        source_detail=v['link'],
                        episode_number=episode,
                        running_total=total_shows
                    )
                    show.total_shows = total_shows
                    show.save()
                else:
                    print('found post ', post.pk, target_date)
                    # post.title = title
                    post.target_date = target_date
                    post.weekday_name = weekday_name
                    post.text = video_link
                    # post.show = show
                    # post.is_active = True
                    post.is_Show = is_show
                    post.is_Politics = is_politics
                    post.is_Joke = is_joke
                    post.is_Quote = is_quote
                    post.tags = tags
                    post.extra_data = extra_data
                    # post.added_by = addedby_user
                    # post.post_author = 'Talk Shows Guru'
                    post.category = show.category
                    post.locale = show.locale
                    post.media_type = 'EMBEDDED_VIDEO'
                    post.source = feed.playlist_link
                    post.source_detail = v['link']

                    dupes_count += 1
                try:
                    post.save()
                    post.country.set(feed.country.all())
                    success_count += 1
                    print(post.post_id, post)

                except IntegrityError:
                    dupes_count += 1
                except Exception:
                    failure_message = sys.exc_info()
                    print("Problems?", failure_message)
                    failed_count += 1

            tend = datetime.now()
            duration = str((tend-tstart).total_seconds() * 1000)
            if failed_count == 0:
                latest_job.job_status = 'SUCCESS'
            else:
                latest_job.job_status = 'FAILED'

            extra_data = {
                'time_start': str(tstart.isoformat()),
                'time_end': str(tend.isoformat()),
                'duration': duration,
                'success': success_count,
                'failed': failed_count,
                'dupes': dupes_count,
                'error': failure_message,
                'previous_extra_data': latest_job.extra_data
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
