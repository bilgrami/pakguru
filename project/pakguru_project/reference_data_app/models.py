# from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from common_utils_app.models import CommonInfo
from pakguru_app.models import Show


class ReferenceSourceType(CommonInfo):
    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'reference_data_source_type'
        verbose_name = 'Source Type'
        verbose_name_plural = 'Source Types'


class ShowReferenceInfo(CommonInfo):
    id = models.AutoField(primary_key=True)
    source_type = models.ForeignKey(ReferenceSourceType,
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True, db_index=True)
    show = models.ForeignKey(Show,
                             on_delete=models.SET_NULL,
                             blank=True, null=True, db_index=True)
    reference_key = models.CharField("Ref Key", max_length=100, null=True,
                                     blank=True)
    number_of_seasons = models.SmallIntegerField("Num of Seasons", null=True,
                                                 blank=True)
    cover_url = models.URLField("Cover URL", null=True, blank=True)
    full_size_cover_url = models.URLField("Full Size Cover URL",
                                          null=True, blank=True)
    cast = JSONField("Cast", null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'reference_data_show_info'
        verbose_name = 'Show'
        verbose_name_plural = 'Shows'


class ShowEpisodeReferenceInfo(CommonInfo):
    id = models.AutoField(primary_key=True)
    source_type = models.ForeignKey(ReferenceSourceType,
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True, db_index=True)
    show = models.ForeignKey(Show,
                             on_delete=models.SET_NULL,
                             blank=True, null=True, db_index=True)
    show_reference_info = models.ForeignKey(ShowReferenceInfo,
                                            on_delete=models.CASCADE,
                                            blank=True, null=True,
                                            db_index=True)
    reference_key = models.CharField(max_length=100, null=True, blank=True)
    season_number = models.SmallIntegerField("Season Number",
                                             null=True, blank=True)
    episode_number = models.SmallIntegerField("Episode Number",
                                              null=True, blank=True)
    running_number = models.SmallIntegerField("Running Number",
                                              null=True, blank=True)
    original_air_date_from_source = models.CharField(max_length=100, null=True,
                                                     blank=True)
    original_air_date = models.DateField(null=True, blank=True)
    year = models.SmallIntegerField(null=True, blank=True)
    series_title = models.CharField("Series Title", max_length=200,
                                    null=True, blank=True)
    episode_title = models.CharField("Episode Title", max_length=200,
                                     null=True, blank=True)
    plot = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'reference_data_show_episode_info'
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'
