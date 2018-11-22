from django.contrib import admin

from .models import Category, News, Resource

admin.site.register(Resource)
admin.site.register(Category)
admin.site.register(News)
