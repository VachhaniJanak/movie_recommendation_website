from django.contrib import admin

from .models import UserInfo, UserWatched, UserLike, UserDislike, UserMyList, RateMovie, UserSession
from django.contrib.sessions.models import Session



# Register your models here.
admin.site.register(UserInfo)
admin.site.register(UserLike)
admin.site.register(UserWatched)
admin.site.register(UserDislike)
admin.site.register(UserMyList)
admin.site.register(RateMovie)
admin.site.register(UserSession)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

admin.site.register(Session, SessionAdmin)