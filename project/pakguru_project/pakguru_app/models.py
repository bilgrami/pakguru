"""
Definition of models.
"""
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from .managers import (ShowManager, JokePostManager,
                       QuotePostManager, PoliticalPostManager)

feed_source_choice = [
    ('Youtube', 'Youtube'),
    ('Talk Shows Central', 'Talk Shows Central'),
    ('unewstv', 'unewstv'),
    ('Facebook', 'Facebook'),
    ('Podcast', 'Podcast'),
    ('Vimeo', 'Vimeo'),
    ('Twitter', 'Twitter'),
    ('Other', 'Other'),
]

media_type_choice = [
    ('text', 'Text'),
    ('image', 'Image'),
    ('video', 'Video'),
    ('podcast', 'Podcast'),
    ('embedded video', 'embedded video'),
    ('document', 'Document'),
]

weekday_choices = [
    ('Sun', 'Sunday'),
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
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

# tvshow_type_choices = [
#     ('Drama', 'Drama'),
#     ('News', 'News'),
#     ('Sports', 'Sports'),
#     ('Cooking', 'Cooking'),
#     ('Movie', 'Movie'),
# ]

# post_category_choices = [
#     (1, 'News TV Show'),
#     (2, 'Joke'),
#     (3, 'Politics'),
#     (4, 'Poetry'),
#     (5, 'News'),
#     (6, 'Quote'),
#     (7, 'Drama Serial'),
# ]


class PostCategoryList(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField("Category Name", max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Post Category"
        verbose_name_plural = "Post Categories"


class LocaleList(models.Model):
    locale_id = models.AutoField(primary_key=True)
    locale_code = models.CharField(max_length=6, default='en-US')
    language = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.locale_code

    class Meta:
        verbose_name_plural = "Locales"


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} <{self.email}>'

    class Meta:
        verbose_name_plural = "Authors"


class CountryList(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField("Country Name", max_length=200)
    short_name = models.CharField("Short Name", max_length=10)
    capital_city = models.CharField("Capital", max_length=100)
    country_phone_code = models.CharField("Country Phone Code",
                                          max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class ShowChannel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    channel_short_code = models.CharField('Channel Code', max_length=20)
    channel_name = models.CharField('Channel Name', max_length=300)
    description = models.TextField('Description', blank=True, null=True)
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
    country = models.ForeignKey(CountryList,
                                related_name='related_show_channels',
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    added_by = models.ForeignKey(User, related_name='related_tvchannel',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.channel_name} ({self.country})'

    class Meta:
        verbose_name = "Show Channel"
        verbose_name_plural = "Show Channels"


class ShowSourceFeed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    feed_name = models.CharField('Feed Name', max_length=300)
    show_name = models.CharField('Show Name', max_length=300)
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
    is_active = models.BooleanField("Is Active", default=True)
    effective_date = models.DateTimeField('Effective Date', auto_now=True)
    expiration_date = models.DateTimeField('Expiration Date',
                                           null=True, blank=True)
    country = models.ManyToManyField(CountryList, blank=True)
    feed_source = models.CharField('Feed Source', choices=feed_source_choice,
                                   max_length=20, null=True, blank=True)
    feed_quality = models.CharField('Max Feed Quality',
                                    choices=feed_quality_choices,
                                    max_length=20, null=True, blank=True)
    priority = models.SmallIntegerField("Priority", default=0)
    extra_data = JSONField(blank=True, null=True)
    added_by = models.ForeignKey(User, related_name='related_tvfeed',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.feed_name} ({self.channel})'

    class Meta:
        verbose_name_plural = "Show Source Feeds"


class Show(models.Model):
    show_id = models.AutoField(primary_key=True)
    show_name = models.CharField('Show Name', max_length=300)
    host_name = models.CharField('Host Name', max_length=300)
    airtime = models.CharField('Air Time', max_length=300,
                               blank=True, null=True)
    website_link = models.URLField('Website', max_length=300,
                                   blank=True, null=True)
    youtube_link = models.URLField('Youtube', max_length=300,
                                   blank=True, null=True)
    facebook_link = models.URLField('Facebook', max_length=300,
                                    blank=True, null=True)
    twitter_link = models.URLField('Twitter', max_length=300,
                                   blank=True, null=True)
    instagram_link = models.URLField('Instagram', max_length=300,
                                     blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
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
    is_active = models.BooleanField("Is Active", default=True)
    effective_date = models.DateTimeField('Effective Date', auto_now=True)
    expiration_date = models.DateTimeField('Expiration Date',
                                           null=True, blank=True)
    country = models.ManyToManyField(CountryList, blank=True)
    extra_data = JSONField(blank=True, null=True)
    added_by = models.ForeignKey(User, related_name='related_youtube_shows',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.channel}] - {self.show_name}'

    class Meta:
        verbose_name_plural = "Shows"


class Post(models.Model):
    post_id = models.AutoField('Post Id', primary_key=True)
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('URL Slug')
    publish_date = models.DateTimeField('Publish Date', auto_now_add=True)
    target_date = models.DateField('Target Date')
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
                             on_delete=models.SET_NULL,
                             blank=True, null=True)
    tags = ArrayField(models.CharField('Tags', max_length=50))
    country = models.ManyToManyField(CountryList, blank=True)
    added_by = models.ForeignKey(User, related_name='related_posts',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    flagged = models.BooleanField("Is Flagged", default=False)
    flagged_data = models.TextField("Flagged Data",
                                    blank=True, null=True)
    extra_data = JSONField(blank=True, null=True)
    created_on = models.DateTimeField('Created On',
                                      auto_now_add=True,
                                      null=True)
    updated = models.DateTimeField(auto_now=True)
    is_Show = models.BooleanField("Is Show", default=True)
    is_Joke = models.BooleanField("Is Joke", default=False)
    is_Quote = models.BooleanField("Is Quote", default=False)
    is_Politics = models.BooleanField("Is Politics", default=False)

    shows = ShowManager()
    jokes = JokePostManager()
    quotes = QuotePostManager()
    politicalposts = PoliticalPostManager()

    def __str__(self):
        dt = self.target_date.strftime("%Y-%m-%d")
        return f'[{dt}] - {self.title}'


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
        verbose_name_plural = "Post Stats"


# class PostViews(models.Model):
#     view_id = models.AutoField('Post View Id', primary_key=True)
#     source_post_id = models.ForeignKey(Post, related_name='related_views',
#                                        on_delete=models.CASCADE)
#     viewed_by = models.CharField('Viewed By', max_length=50, blank=True,
#                                  null=True)
#     rating = models.SmallIntegerField('Rating', default=0)
