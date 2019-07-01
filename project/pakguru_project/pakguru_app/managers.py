from django.db import models


class ShowManager(models.Manager):
    def get_queryset(self):
        return super(ShowManager, self).get_queryset()\
                          .filter(is_Show=True)


class JokePostManager(models.Manager):
    def get_queryset(self):
        return super(JokePostManager, self).get_queryset()\
                          .filter(is_Joke=True)


class QuotePostManager(models.Manager):
    def get_queryset(self):
        return super(QuotePostManager, self).get_queryset()\
                          .filter(is_Quote=True)


class PoliticalPostManager(models.Manager):
    def get_queryset(self):
        return super(PoliticalPostManager, self).get_queryset()\
                          .filter(is_Politics=True)
