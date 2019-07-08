from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class CommonInfo(models.Model):
    name = models.CharField('Name', max_length=300,
                            db_index=True, blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
    is_active = models.BooleanField('Is Active', default=True, db_index=True)
    effective_date = models.DateTimeField('Effective Date', auto_now=True)
    expiration_date = models.DateTimeField('Expiration Date',
                                           null=True, blank=True)
    added_by = models.ForeignKey(User,
                                 related_name="%(app_label)s_%(class)s_related",  # noqa: E501
                                 related_query_name="%(app_label)s_%(class)ss",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    extra_data = JSONField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['name']
