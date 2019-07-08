from django.contrib import admin
from .models import (ReferenceSourceType,
                     ShowReferenceInfo,
                     ShowEpisodeReferenceInfo)

admin.site.register(ReferenceSourceType)
admin.site.register(ShowReferenceInfo)
admin.site.register(ShowEpisodeReferenceInfo)
