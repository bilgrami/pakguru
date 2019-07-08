from django.contrib import admin
from .models import (ReferenceSourceType,
                     ShowReferenceInfo,
                     ShowEpisodeReferenceInfo)

admin.site.register(ReferenceSourceType)
admin.site.register(ShowReferenceInfo)


@admin.register(ShowEpisodeReferenceInfo)
class ShowEpisodeReferenceInfo(admin.ModelAdmin):
    list_display = ('name', 'source_type', 'show',
                    'season_number', 'running_number',
                    'episode_number', 'original_air_date',
                    'added_by', 'updated')
    list_filter = ('source_type', 'show_reference_info', 'season_number')
    search_fields = ('source_type__name', 'name', 'running_number')
    date_hierarchy = 'original_air_date'
    ordering = ('show', 'season_number', 'episode_number',)
    list_per_page = 100
    readonly_fields = ('id', 'created', 'updated', 'effective_date',)
    fields = ('id', 'name', 'description',
              'source_type', 'show',
              'show_reference_info',
              'reference_key',
              'season_number',
              'episode_number',
              'running_number',
              'original_air_date',
              'original_air_date_from_source',
              'series_title', 'episode_title',
              'plot',
              'is_active',
              'expiration_date',
              'extra_data',
              'added_by', 'updated')
    save_on_top = True
