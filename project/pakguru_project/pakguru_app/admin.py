from django.contrib import admin

from .models import (Author, PostCategoryList,
                     LocaleList, Post, ShowSourceFeed,
                     Show, CountryList, ShowChannel, PostStats)

admin.site.register(Author)
admin.site.register(PostCategoryList)
admin.site.register(LocaleList)
admin.site.register(Show)
admin.site.register(ShowSourceFeed)
admin.site.register(Post)
admin.site.register(CountryList)
admin.site.register(ShowChannel)
admin.site.register(PostStats)
