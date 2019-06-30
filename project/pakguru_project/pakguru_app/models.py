"""
Definition of models.
"""
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from .managers import DailyTVManager, JokePostManager, QuotePostManager

media_type_choice = [
    ('text', 'Text'),
    ('image', 'Image'),
    ('video', 'Video'),
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


class CountryList(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField("Country Name", max_length=200)
    short_name = models.CharField("Short Name", max_length=10)
    capital_city = models.CharField("Capital", max_length=100)
    country_phone_code = models.CharField("country_phone_code", max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class YouTubeFeed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    show_name = models.CharField('Show Name', max_length=300)
    feed_name = models.CharField('Show Name', max_length=300)
    channel_short_code = models.CharField('Channel Code', max_length=10)
    channel_name = models.CharField('Channel Name', max_length=300)
    channel_link = models.URLField('Channel Link', max_length=500)
    playlist_link = models.URLField('Playlist Link', max_length=500)
    latest_show_link = models.URLField('Latest Show Link', max_length=500, null=True, blank=True)
    search_pattern = models.CharField('Search Pattern', max_length=500, null=True, blank=True)
    search_url = models.URLField('Search URL', max_length=500, null=True, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    expiration_date = models.DateTimeField('Expiration Date', null=True, blank=True)
    added_by = models.ForeignKey(User, related_name='related_youtube_feeds',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    country = models.ManyToManyField(CountryList, blank=True, null=True)
    feed_quality = models.CharField('Feed Quality', max_length=50)
    priority = models.SmallIntegerField("Priority")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    extra_data = JSONField()

    class Meta:
        verbose_name_plural = "Youtube Feeds"


class YouTubeShow(models.Model):
    show_id = models.AutoField(primary_key=True)
    show_name = models.CharField('Show Name', max_length=300)
    host_name = models.CharField('Host Name', max_length=300)
    description = models.TextField('Description')
    channel_short_code = models.CharField('Channel Code', max_length=10)
    channel_name = models.CharField('Channel Name', max_length=300)
    channel_link = models.URLField('Channel Link', max_length=500)
    playlist_link = models.URLField('Playlist Link', max_length=500)
    latest_show_link = models.URLField('Latest Show Link', max_length=500, null=True, blank=True)
    search_pattern = models.CharField('Search Pattern', max_length=500, null=True, blank=True)
    search_url = models.URLField('Search URL', max_length=500, null=True, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    expiration_date = models.DateTimeField('Expiration Date', null=True, blank=True)
    added_by = models.ForeignKey(User, related_name='related_youtube_shows',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    country = models.ManyToManyField(CountryList, blank=True, null=True)
    feed_quality = models.CharField('Feed Quality', max_length=50)
    priority = models.SmallIntegerField("Priority")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    youtube_feed_list = models.ManyToManyField(YouTubeFeed,
                                               related_name='youtube_shows')
    extra_data = JSONField()

    class Meta:
        verbose_name_plural = "Youtube Shows"


class Post(models.Model):
    post_id = models.AutoField('Post Id', primary_key=True)
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('URL Slug')
    text = models.TextField('Text')
    post_author = models.CharField('Author', max_length=255)
    source = models.CharField('Source', max_length=255)
    source_detail = models.TextField('Source Detail')
    category = models.ForeignKey(PostCategoryList,
                                 related_name='related_posts',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    media_type = models.CharField('Media Type',
                                  max_length=50,
                                  choices=media_type_choice,
                                  default='text')
    publish_date = models.DateTimeField('Publish Date')
    weekday_name = models.CharField('Weekday', max_length=3,
                                    choices=weekday_choices)
    locale = models.ForeignKey(LocaleList,
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    youtube_show = models.ForeignKey(YouTubeShow,
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)
    tags = ArrayField(models.CharField('Tags', max_length=50))
    added_by = models.ForeignKey(User, related_name='related_posts',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    country = models.ManyToManyField(CountryList, blank=True, null=True)
    created_on = models.DateTimeField('Created On',
                                      auto_now_add=True,
                                      null=True)
    extra_data = JSONField()

    # daily_tv = DailyTVManager()
    # jokes = JokePostManager()
    # quotes = QuotePostManager()

# class PostStats(models.Model):
#     post_stat_id = models.AutoField('Post Stat Id', primary_key=True)
#     post_id = models.ForeignKey(Post, related_name='related_stats',
#                                 on_delete=models.CASCADE)
#     total_views = models.IntegerField('Total Views', default=0)


# class PostViews(models.Model):
#     view_id = models.AutoField('Post View Id', primary_key=True)
#     source_post_id = models.ForeignKey(Post, related_name='related_views',
#                                        on_delete=models.CASCADE)
#     viewed_by = models.CharField('Viewed By', max_length=50, blank=True,
#                                  null=True)
#     rating = models.SmallIntegerField('Rating', default=0)
