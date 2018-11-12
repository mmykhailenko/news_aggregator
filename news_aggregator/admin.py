from django.contrib import admin

from .models import Category, User, News, Resource

admin.site.register(Resource)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(News)
