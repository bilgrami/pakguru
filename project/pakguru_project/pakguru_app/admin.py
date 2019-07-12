from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, ShowSourceFeed,
                     Show, CountryList, ShowChannel, PostStatistic,
                     ShowFeed_HarvestJobLog, FeedSourceType)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(CountryList)
admin.site.register(ShowChannel)
admin.site.register(PostStatistic)
admin.site.register(FeedSourceType)


@admin.register(ShowFeed_HarvestJobLog)
class ShowFeed_HarvestJobLog(admin.ModelAdmin):
    list_display = ('job_id', 'show_feed',
                    'latest_feed_date',
                    'is_latest', 'feed_data',
                    'job_status',
                    'added_by', 'updated')
    list_filter = ('show_feed__feed_source_type', 'is_latest', 'job_status')
    search_fields = ('job_id', 'show_feed__name',
                     'show_feed__feed_source_type__name')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 50
    readonly_fields = ('created', 'updated')
    fields = ('show_feed',
              'latest_feed_date',
              'feed_data',
              'is_latest',
              'job_status',
              'notes',
              'extra_data',
              'added_by', 'updated')
    save_on_top = True


@admin.register(ShowSourceFeed)
class ShowSourceFeed(admin.ModelAdmin):
    list_display = ('feed_id', 'name',
                    'show_name',
                    'channel', 'is_active', 'feed_source_type',
                    'feed_quality', 'priority', 'updated')
    list_filter = ('feed_source_type', 'channel', 'is_active', 'country')
    search_fields = ('feed_id', 'name', 'channel__name')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 30
    readonly_fields = ('created', 'effective_date', 'updated',)
    fields = ('name', 'show_name', 'channel',
              'playlist_link', 'latest_show_link',
              'title_example', 'title_search_pattern',
              'search_api_url', 'search_api_pattern',
              'expiration_date',
              'country',
              'is_active', 'feed_source_type',
              'feed_quality', 'priority',
              'added_by', 'extra_data',)
    save_on_top = True


@admin.register(Show)
class Show(admin.ModelAdmin):
    list_display = ('show_id', 'name', 'show_host',
                    'category', 'primary_feed',
                    'channel', 'locale',
                    'is_active', 'total_shows')
    list_filter = ('channel', 'primary_feed__feed_source_type',
                   'category', 'country__name', 'is_active', 'locale')
    search_fields = ('show_id', 'name', 'host_name',
                     'description')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 30
    readonly_fields = ('show_id', 'created', 'effective_date', 'updated',)
    fields = ('show_id', 'name', 'host_name',
              'airtime', 'website_link',
              'youtube_link', 'facebook_link',
              'twitter_link', 'instagram_link',
              'description',
              'category',
              'channel', 'locale',
              'is_active',
              'primary_feed',
              'additional_feeds',
              'expiration_date', 'country',
              'added_by', 'extra_data', 'total_shows'
              )
    save_on_top = True

    def get_ellipses(self, data, n):
        return (data[:n] + '..') if len(data) > n else data

    def show_host(self, obj):
        return self.get_ellipses(obj.host_name, 20)


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('post_id', 'title',
                    'target_date', 'publish_date',
                    'show',
                    'category', 'locale', 'weekday_name',
                    'episode_number', 'running_total',
                    'is_active', 'flagged',
                    'is_Show', 'is_Joke', 'is_Quote', 'is_Politics')
    list_filter = ('target_date', 'weekday_name', 'category',
                   'is_active', 'flagged', 'is_Show', 'is_Joke',
                   'is_Quote', 'is_Politics')
    search_fields = ('post_id', 'title',)
    date_hierarchy = 'target_date'
    ordering = ('-target_date', '-publish_date',)
    list_per_page = 100
    readonly_fields = ('created', 'publish_date', 'updated',)
    fields = ('title', 'slug',
              'publish_date',
              'target_date',
              'text',
              'post_author',
              'source',
              'source_detail',
              'category',
              'media_type', 'weekday_name',
              'locale',
              'show',
              'tags',
              'country',
              'is_active', 'flagged',
              'flagged_data',
              'extra_data',
              'is_Show', 'is_Joke', 'is_Quote', 'is_Politics',
              'episode_number', 'running_total'
              )
    save_on_top = True

    def get_ellipses(self, data, n):
        return (data[:n] + '..') if len(data) > n else data

    def get_title(self, obj):
        return self.get_ellipses(obj.title, 20)
