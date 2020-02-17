from datetime import datetime

import django.utils.text
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.urls import reverse

from common_utils_app.models import CommonInfo

joblog_status_choices = [
    ('NOT STARTED', 'Not Started'),
    ('IN PROGRESS', 'In Progress'),
    ('SUCCESS', 'Success'),
    ('FAILED', 'Failed'),
    ('PAUSED', 'Paused'),
    ('CANCELLED', 'Cancelled'),
]

media_type_choice = [
    ('TEXT', 'Text'),
    ('IMAGE', 'Image'),
    ('VIDEO', 'Video'),
    ('PODCAST', 'Podcast'),
    ('EMBEDDED_VIDEO', 'embedded video'),
    ('DOCUMENT', 'Document'),
]

weekday_choices = [
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
]

feed_quality_choices = [
    ('320p', '320p'),
    ('480p', '480p'),
    ('720p', '720p'),
    ('1080p', '1080p'),
    ('HD', 'HD'),
    ('4K', '4K'),
    ('8K', '8K'),
]

feed_frequency_choices = [
    ('ONE_TIME', 'once'),
    ('DAILY', 'Daily')
]


class PostCategoryList(CommonInfo):
    category_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pakguru_app_postcategorylist'
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'


class LocaleList(models.Model):
    locale_id = models.AutoField(primary_key=True)
    locale_code = models.CharField(max_length=6, default='en-US')
    language = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.locale_code

    class Meta:
        verbose_name_plural = 'Locales'


class Author(CommonInfo):
    author_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} <{self.email}>'

    class Meta:
        db_table = 'pakguru_app_author'
        verbose_name_plural = 'Authors'


class CountryList(CommonInfo):
    country_id = models.AutoField(primary_key=True)
    short_name = models.CharField('Short Name', max_length=10)
    capital_city = models.CharField('Capital', max_length=100)
    country_phone_code = models.CharField('Country Phone Code',
                                          max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pakguru_app_countrylist'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class ShowCommonInfo(CommonInfo):
    website_link = models.URLField('Website', max_length=500,
                                   blank=True, null=True)
    youtube_link = models.URLField('Youtube', max_length=300,
                                   blank=True, null=True)
    facebook_link = models.URLField('Facebook', max_length=300,
                                    blank=True, null=True)
    twitter_link = models.URLField('Twitter', max_length=300,
                                   blank=True, null=True)
    instagram_link = models.URLField('Instagram', max_length=300,
                                     blank=True, null=True)
    country = models.ManyToManyField(CountryList, blank=True,
                                     related_name="%(app_label)s_%(class)s_related",  # noqa: E501
                                     related_query_name="%(app_label)s_%(class)ss",  # noqa: E501
                                    )

    class Meta:
        abstract = True
        ordering = ['name']


class ShowChannel(ShowCommonInfo):
    channel_id = models.AutoField(primary_key=True)
    channel_short_code = models.CharField('Channel Code', max_length=20,
                                          db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'pakguru_app_showchannel'
        verbose_name = 'Show Channel'
        verbose_name_plural = 'Show Channels'


class FeedSourceType(CommonInfo):
    short_code = models.CharField('Short Code', max_length=3, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pakguru_app_feedsourcetype'
        verbose_name = 'Feed Source Type'
        verbose_name_plural = 'Feed Source Types'


class ShowSourceFeed(CommonInfo):
    feed_id = models.AutoField(primary_key=True)
    show_name = models.CharField('Show Name', max_length=300, db_index=True)
    channel = models.ForeignKey(ShowChannel,
                                on_delete=models.SET_NULL,
                                blank=True, null=True)
    playlist_link = models.URLField('Playlist Link', max_length=500)
    latest_show_link = models.URLField('Latest Show Link', max_length=500,
                                       null=True, blank=True)
    title_example = models.CharField('Title Example', max_length=500,
                                     null=True, blank=True)
    title_search_pattern = models.CharField('Title Search Pattern',
                                            max_length=500,
                                            null=True, blank=True)
    search_api_url = models.URLField('Search URL', max_length=500,
                                     null=True, blank=True)
    search_api_pattern = models.CharField('Search Pattern', max_length=500,
                                          null=True, blank=True)
    country = models.ManyToManyField(CountryList, blank=True, db_index=True)
    feed_source_type = models.ForeignKey(FeedSourceType,
                                         on_delete=models.CASCADE,
                                         null=True, blank=True)
    feed_quality = models.CharField('Max Feed Quality',
                                    choices=feed_quality_choices,
                                    max_length=20, null=True, blank=True)
    priority = models.SmallIntegerField('Priority', default=0)
    feed_frequency = models.CharField('Feed Frequency',
                                      max_length=20,
                                      choices=feed_frequency_choices,
                                      default='ONE_TIME')

    def __str__(self):
        return f'{self.name} ({self.channel})'

    class Meta:
        db_table = 'pakguru_app_showsourcefeed'
        verbose_name_plural = 'Show Source Feeds'


def data_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    dt = datetime.today()
    year = dt.strftime('%Y')
    today = dt.strftime('%Y-%m-%d')
    folder = year + '/' + today
    user = 'unknown-user'
    if instance and instance.added_by:
        user = f'{instance.added_by.id}-{instance.added_by}'
    file_name = f'{today}-{user}-{filename}'
    return 'datafiles/{0}/{1}'.format(folder, file_name)


class ShowFeed_HarvestJobLog(CommonInfo):
    job_id = models.AutoField(primary_key=True)
    show_feed = models.ForeignKey(ShowSourceFeed,
                                  on_delete=models.CASCADE)
    latest_feed_date = models.DateField('Latest Feed Date', db_index=True)
    is_latest = models.BooleanField('Is Latest', default=True, db_index=True)
    feed_data = models.FileField(upload_to=data_file_directory_path,
                                 null=True, blank=True)
    job_status = models.CharField('Job Status',
                                  max_length=20,
                                  choices=joblog_status_choices,
                                  default='NOT STARTED')
    notes = models.TextField("Additional Notes",
                             null=True, blank=True)

    def __str__(self):
        return f'{str(self.latest_feed_date)} - [{self.show_feed}]'

    class Meta:
        db_table = 'pakguru_app_showfeed_harvestjoblog'
        verbose_name = 'Feed Harvest Job'
        verbose_name_plural = 'Feed Harvest Jobs'


class Show(ShowCommonInfo):
    show_id = models.AutoField(primary_key=True)
    host_name = models.CharField('Host Name', max_length=300)
    airtime = models.CharField('Air Time', max_length=300,
                               blank=True, null=True)
    category = models.ForeignKey(PostCategoryList,
                                 related_name='related_tvshow',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    channel = models.ForeignKey(ShowChannel,
                                on_delete=models.SET_NULL,
                                blank=True, null=True)
    primary_feed = models.ForeignKey(ShowSourceFeed,
                                     on_delete=models.SET_NULL,
                                     related_name='related_primary_shows',
                                     blank=True, null=True)
    additional_feeds = models.ManyToManyField(ShowSourceFeed,
                                              related_name='related_shows',
                                              blank=True)
    locale = models.ForeignKey(LocaleList,
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    total_shows = models.SmallIntegerField('Total Shows', default=-1,
                                           blank=True, null=True)

    def __str__(self):
        return f'[{self.channel}] - {self.name}'

    # def get_absolute_url(self):
    #     return reverse('show_detail', args=[str(self.show_id)])

    class Meta:
        db_table = 'pakguru_app_show'
        verbose_name_plural = 'Shows'


class Post(CommonInfo):
    post_id = models.AutoField('Post Id', primary_key=True)
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('URL Slug', max_length=255, unique=True)
    publish_date = models.DateTimeField('Publish Date', auto_now_add=True)
    target_date = models.DateTimeField('Target Date', db_index=True)
    text = models.TextField('Text',
                            blank=True, null=True)
    post_author = models.CharField('Author', max_length=255,
                                   blank=True, null=True)
    source = models.CharField('Source', max_length=255,
                              blank=True, null=True)
    source_detail = models.TextField('Source Detail',
                                     blank=True, null=True)
    category = models.ForeignKey(PostCategoryList,
                                 related_name='related_posts',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    media_type = models.CharField('Media Type',
                                  max_length=50,
                                  choices=media_type_choice,
                                  default='text')
    weekday_name = models.CharField('Weekday', max_length=3,
                                    choices=weekday_choices)
    locale = models.ForeignKey(LocaleList,
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    show = models.ForeignKey(Show,
                             on_delete=models.CASCADE, db_index=True)
    tags = ArrayField(models.CharField('Tags', max_length=50,
                                       blank=True, null=True, db_index=True))
    country = models.ManyToManyField(CountryList, blank=True)
    flagged = models.BooleanField('Flagged',
                                  default=False, db_index=True)
    flagged_data = models.TextField('Flag Info',
                                    blank=True, null=True)
    is_Show = models.BooleanField('Is Show', default=True)
    is_Joke = models.BooleanField('Is Joke', default=False)
    is_Quote = models.BooleanField('Is Quote', default=False)
    is_Politics = models.BooleanField('Is Political', default=False)
    episode_number = models.SmallIntegerField('Episode Number', default=-1,
                                              blank=True, null=True,
                                              db_index=True)
    running_total = models.SmallIntegerField('Running Total', default=-1,
                                             blank=True, null=True,
                                             db_index=True)

    # shows = ShowManager()
    # jokes = JokePostManager()
    # quotes = QuotePostManager()
    # politicalposts = PoliticalPostManager()

    def __str__(self):
        dt = self.target_date.strftime('%Y-%m-%d')
        return f'[{dt}] - {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[django.utils.text.slugify(self.show.channel),
                             django.utils.text.slugify(self.show),
                             self.slug,
                             str(self.post_id)])

    class Meta:
        db_table = 'pakguru_app_post'
        verbose_name_plural = 'Posts'


class PostStatistic(models.Model):
    post_stat_id = models.AutoField('Post Stat Id', primary_key=True)
    post_id = models.ForeignKey(Post, related_name='related_stats',
                                on_delete=models.CASCADE)
    total_views = models.IntegerField('Total Views', default=0)
    up_votes = models.IntegerField('Up', default=0)
    down_votes = models.IntegerField('Down', default=0)
    down_votes = models.IntegerField('Down', default=0)
    extra_data = JSONField(blank=True, null=True)
    created_on = models.DateTimeField('Created On',
                                      auto_now_add=True,
                                      null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Post Stats'

# class PostViews(models.Model):
#     view_id = models.AutoField('Post View Id', primary_key=True)
#     source_post_id = models.ForeignKey(Post, related_name='related_views',
#                                        on_delete=models.CASCADE)
#     viewed_by = models.CharField('Viewed By', max_length=50, blank=True,
#                                  null=True)
#     rating = models.SmallIntegerField('Rating', default=0)
