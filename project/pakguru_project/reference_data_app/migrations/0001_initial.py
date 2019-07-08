# Generated by Django 2.2.3 on 2019-07-08 10:12

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pakguru_app', '0006_auto_20190706_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceSourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Is Active')),
                ('effective_date', models.DateTimeField(auto_now=True, verbose_name='Effective Date')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Expiration Date')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reference_data_app_referencesourcetype_related', related_query_name='reference_data_app_referencesourcetypes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Source Type',
                'verbose_name_plural': 'Source Types',
                'db_table': 'reference_data_source_type',
            },
        ),
        migrations.CreateModel(
            name='ShowReferenceInfo',
            fields=[
                ('name', models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Is Active')),
                ('effective_date', models.DateTimeField(auto_now=True, verbose_name='Effective Date')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Expiration Date')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reference_key', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ref Key')),
                ('number_of_seasons', models.SmallIntegerField(blank=True, null=True, verbose_name='Num of Seasons')),
                ('cover_url', models.URLField(blank=True, null=True, verbose_name='Cover URL')),
                ('full_size_cover_url', models.URLField(blank=True, null=True, verbose_name='Full Size Cover URL')),
                ('cast', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Cast')),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reference_data_app_showreferenceinfo_related', related_query_name='reference_data_app_showreferenceinfos', to=settings.AUTH_USER_MODEL)),
                ('show', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pakguru_app.Show')),
                ('source_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference_data_app.ReferenceSourceType')),
            ],
            options={
                'verbose_name': 'Show Info',
                'verbose_name_plural': 'Show Infosets',
                'db_table': 'reference_data_show_info',
            },
        ),
        migrations.CreateModel(
            name='ShowEpisodeReferenceInfo',
            fields=[
                ('name', models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Is Active')),
                ('effective_date', models.DateTimeField(auto_now=True, verbose_name='Effective Date')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Expiration Date')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reference_key', models.CharField(blank=True, max_length=100, null=True)),
                ('season_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Season Number')),
                ('episode_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Episode Number')),
                ('running_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Running Number')),
                ('original_air_date_from_source', models.CharField(blank=True, max_length=100, null=True)),
                ('original_air_date', models.DateField(blank=True, null=True)),
                ('year', models.SmallIntegerField(blank=True, null=True)),
                ('series_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Series Title')),
                ('episode_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Episode Title')),
                ('plot', models.CharField(blank=True, max_length=100, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reference_data_app_showepisodereferenceinfo_related', related_query_name='reference_data_app_showepisodereferenceinfos', to=settings.AUTH_USER_MODEL)),
                ('show', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pakguru_app.Show')),
                ('show_reference_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reference_data_app.ShowReferenceInfo')),
                ('source_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference_data_app.ReferenceSourceType')),
            ],
            options={
                'verbose_name': 'Episode Info',
                'verbose_name_plural': 'Episode Infosets',
                'db_table': 'reference_data_show_episode_info',
            },
        ),
    ]