from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, YouTubeFeed,
                     YouTubeShow, CountryList)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(YouTubeShow)
admin.site.register(YouTubeFeed)
admin.site.register(Post)
admin.site.register(CountryList)
