from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, YouTubeFeeds)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(YouTubeFeeds)
admin.site.register(Post)
