from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(IdeaType)
admin.site.register(Status)
admin.site.register(Keyword)
admin.site.register(Photo)

class IdeaAdmin(admin.ModelAdmin):
    readonly_fields = ('CreatedDate',)

admin.site.register(Idea,IdeaAdmin)

admin.site.register(UserProfile)
admin.site.register(UserLike)