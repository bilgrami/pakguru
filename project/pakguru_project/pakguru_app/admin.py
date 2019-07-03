from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, ShowSourceFeed,
                     Show, CountryList, ShowChannel, PostStatistic,
                     ShowFeed_HarvestJobLog)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(Post)
admin.site.register(CountryList)
admin.site.register(ShowChannel)
admin.site.register(PostStatistic)


@admin.register(ShowFeed_HarvestJobLog)
class ShowFeed_HarvestJobLog(admin.ModelAdmin):
    list_display = ('job_id', 'feed_id',
                    'latest_feed_date',
                    'is_latest', 'feed_data',
                    'job_status',
                    'added_by', 'updated')
    list_filter = ('feed_id__feed_source', 'is_latest', 'job_status')
    search_fields = ('job_id', 'feed_id', 'feed_id__feed_source')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 50
    readonly_fields = ('created', 'updated')
    fields = ('feed_id',
              'latest_feed_date',
              'feed_data',
              'is_latest',
              'job_status',
              'notes',
              'added_by', 'updated')
    save_on_top = True


@admin.register(ShowSourceFeed)
class ShowSourceFeed(admin.ModelAdmin):
    list_display = ('feed_id', 'feed_name',
                    'show_name',
                    'channel', 'is_active', 'feed_source',
                    'feed_quality', 'priority', 'updated')
    list_filter = ('feed_source', 'channel', 'is_active', 'country')
    search_fields = ('feed_name', 'channel__channel_name', 'show_name')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 30
    readonly_fields = ('created', 'effective_date', 'updated',)
    fields = ('feed_name', 'show_name', 'channel',
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
    list_display = ('show_name', 'get_host_name',
                    'category', 'primary_feed',
                    'channel', 'locale',
                    'is_active')
    list_filter = ('country__name', 'show_name', 'is_active',
                   'channel',)
    search_fields = ('show_name', 'host_name',
                     'description')
    date_hierarchy = 'updated'
    ordering = ('-updated',)
    list_per_page = 30
    readonly_fields = ('created', 'effective_date', 'updated',)
    fields = ('show_name', 'host_name',
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

    def get_host_name(self, obj):
        return self.get_ellipses(obj.host_name, 20)

    # def get_primary_feed(self, obj):
    #     return self.get_ellipses(obj.primary_feed__feed_name, 20)
