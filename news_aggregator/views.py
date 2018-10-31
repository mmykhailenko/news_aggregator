from django.views import generic
from .models import User, News, Tag, Category, Resource


class NewsView(generic.ListView):

    model = News
    template_name = 'news_list'


class UserView(generic.ListView):

    model = User
    template_name = 'user_list'


class TagView(generic.ListView):

    model = Tag
    template_name = 'tag_list'


class CategoryView(generic.ListView):

    model = Category
    template_name = 'category_list'


class ResourceView(generic.ListView):

    model = Resource
    template_name = 'resource_list'
