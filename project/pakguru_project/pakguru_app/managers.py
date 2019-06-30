from django.db import models


class DailyTVManager(models.Manager):
    def get_queryset(self):
        return super(DailyTVManager, self).get_queryset()\
                          .filter(category='Daily TV')


class JokePostManager(models.Manager):
    def get_queryset(self):
        return super(JokePostManager, self).get_queryset()\
                          .filter(category='Joke')


class QuotePostManager(models.Manager):
    def get_queryset(self):
        return super(QuotePostManager, self).get_queryset()\
                          .filter(category='Quote')
