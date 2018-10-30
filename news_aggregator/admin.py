from django.contrib import admin

from .models import News, User, Tag, Resource

admin.site.register(News)
admin.site.register(Tag)
admin.site.register(Resource)
admin.site.register(User)



