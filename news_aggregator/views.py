from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Resource, News


class ResourceListView(ListView):
    model = Resource
    template_name = 'news_aggregator/resource_list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        return Resource.objects.all()


class CategoryListView(ListView):
    model = Category
    template_name = 'news_aggregator/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class NewsListView(ListView):
    model = News
    template_name = 'news_aggregator/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.all()


class NewsDetailView(DetailView):
    model = News
    template_name = 'news_aggregator/news_single.html'


class NewsByCategoryListView(ListView):
    model = News
    template_name = 'news_aggregator/news_category_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category_name'))
        return News.objects.filter(category=category)


def documentation_view(request):
    if request.method == 'GET':
        return render(request, 'news_aggregator/docs.html')
