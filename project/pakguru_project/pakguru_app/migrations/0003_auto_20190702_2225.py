# Generated by Django 2.2.3 on 2019-07-03 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pakguru_app', '0002_showfeed_harvestjoblog_extra_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='showfeed_harvestjoblog',
            old_name='feed_id',
            new_name='show_feed',
        ),
    ]
