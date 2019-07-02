from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, ShowSourceFeed,
                     Show, CountryList, ShowChannel, PostStatistic)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(Show)
admin.site.register(Post)
admin.site.register(CountryList)
admin.site.register(ShowChannel)
admin.site.register(PostStatistic)


@admin.register(ShowSourceFeed)
class ShowSourceFeed(admin.ModelAdmin):
    list_display = ('feed_name',
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
