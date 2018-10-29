from django.contrib import admin

from .models import Category, Tag, User, News, Resource

admin.site.register(Resource)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(News)
