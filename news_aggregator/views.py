from django.views import generic
from .models import User, News, Tag, Category, Resource


class NewsView(generic.ListView):

    model = News


class NewsDetailView(generic.DetailView):

    model = News
    context_object_name = 'news'


class UserView(generic.ListView):

    model = User


class TagView(generic.ListView):

    model = Tag


class CategoryView(generic.ListView):

    model = Category


class ResourceView(generic.ListView):

    model = Resource
