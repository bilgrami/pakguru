from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, ShowSourceFeed,
                     Show, CountryList, ShowChannel, PostStatistic,
                     ShowFeed_HarvestJobLog)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(CountryList)
admin.site.register(ShowChannel)
admin.site.register(PostStatistic)


@admin.register(ShowFeed_HarvestJobLog)
class ShowFeed_HarvestJobLog(admin.ModelAdmin):
    list_display = ('job_id', 'show_feed',
                    'latest_feed_date',
                    'is_latest', 'feed_data',
                    'job_status',
                    'added_by', 'updated')
    list_filter = ('show_feed__feed_source', 'is_latest', 'job_status')
    search_fields = ('job_id', 'show_feed__name', 'show_feed__feed_source')
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
                    'channel', 'is_active', 'feed_source',
                    'feed_quality', 'priority', 'updated')
    list_filter = ('feed_source', 'channel', 'is_active', 'country')
    search_fields = ('feed_name', 'channel__channel_name', 'name')
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
              'is_active', 'feed_source',
              'feed_quality', 'priority',
              'added_by', 'extra_data',)
    save_on_top = True


@admin.register(Show)
class Show(admin.ModelAdmin):
    list_display = ('name', 'show_host',
                    'category', 'primary_feed',
                    'channel', 'locale',
                    'is_active')
    list_filter = ('country__name', 'name', 'is_active',
                   'channel',)
    search_fields = ('name', 'host_name',
                     'description')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 30
    readonly_fields = ('created', 'effective_date', 'updated',)
    fields = ('name', 'host_name',
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
              'added_by', 'extra_data'
              )
    save_on_top = True

    def get_ellipses(self, data, n):
        return (data[:n] + '..') if len(data) > n else data

    def show_host(self, obj):
        return self.get_ellipses(obj.host_name, 20)


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title',
                    'target_date', 'publish_date',
                    'category', 'locale', 'weekday_name',
                    'is_active', 'flagged',
                    'is_Show', 'is_Joke', 'is_Quote', 'is_Politics')
    list_filter = ('target_date', 'weekday_name', 'category', 'is_active',
                   'flagged', 'is_Show', 'is_Joke', 'is_Quote', 'is_Politics')
    search_fields = ('title',)
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
              'is_Show', 'is_Joke', 'is_Quote', 'is_Politics'
              )
    save_on_top = True

    def get_ellipses(self, data, n):
        return (data[:n] + '..') if len(data) > n else data

    def get_title(self, obj):
        return self.get_ellipses(obj.title, 20)
