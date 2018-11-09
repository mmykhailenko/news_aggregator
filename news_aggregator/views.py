from datetime import date
from django.shortcuts import render
from django.core.exceptions import FieldError
from django.http import HttpResponseBadRequest
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


class NewsByFilterListView(ListView):
    model = News
    template_name = 'news_aggregator/news_filter_list.html'
    context_object_name = 'news'

    def _bad_request(self, *bad_values):
        return HttpResponseBadRequest(content=f'{bad_values} is not valid to this request!')

    def _extract_date(self, value):
        """ Parse date data from value """
        passed = value
        try:
            value = [int(val) for val in value.split('-')]
            return date(*value)
        except (ValueError, TypeError):
            return self._bad_request(passed)  # TODO send appropriate response to user

    def get_queryset(self):
        """
        Get values passed in url and return filtered list of News object. Case is insensitive

        possible values for 'field_name' url parameter:
            'title' -  search news with given title (i.g. 'tittle=odessa')
            'category' - search news for given category name (i.g. 'category=sport')
            'country' - search news for given resource country name (i.g. 'country=Germany')
            'from' - search news from given date to current. This date should be in ISO 8601 format (YYYY-MM-DD)
                    (e.g. from=2018-11-09)
            'until' - search news from oldest date to given (e.g. until=2018-11-09)
        """
        filter_modifier = '__iexact'  # Makes search case insensitive
        value = self.kwargs.get('value')
        field = self.kwargs.get('field_name')
        if field == 'category':
            field += '_id__name' + filter_modifier
        elif field == 'country':
            field = 'resource__' + field + filter_modifier
        elif field == 'from':
            field = 'date__gt'
            value = self._extract_date(value)
        elif field == 'until':
            field = 'date__lt'
            value = self._extract_date(value)
        try:
            return News.objects.filter(**{field: value})
        except FieldError:
            return self._bad_request(field)  # TODO send appropriate response to user


def documentation_view(request):
    if request.method == 'GET':
        return render(request, 'news_aggregator/docs.html')
