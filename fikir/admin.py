from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(IdeaType)
admin.site.register(Status)
admin.site.register(Address)
admin.site.register(Keyword)
admin.site.register(Photo)
admin.site.register(Idea)
admin.site.register(UserProfile)
admin.site.register(UserLike)