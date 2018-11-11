from datetime import date
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
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


class NewsQueries:
    """
    Implement utility methods for constructing query params

    For compatibility all methods implemented here should return:
        tuple:('<model field/relative_model_field[__search modifier]>', <search value>, <status_code>)
        E.g.: ('category_id__name', 'health', 200)
              ('title', 'Trump', 200)
              ('date__gt', '2010-01-01', 200)
              ('date_gt', '2010-01-01', 400)
              ('date__lt', 'not_a_date', 400)

    For more info about possible queries in Django visit: https://docs.djangoproject.com/en/2.1/topics/db/queries/
    """
    FILTER_MODIFIER = '__iexact'  # Makes search case insensitive

    def _category_query(self, value):
        """ Return query params for news filtered by category value. Value passed here for compatibility"""
        return 'category_id__name' + self.FILTER_MODIFIER, value, 200

    def _country_query(self, value):
        """ Return query params for news filtered by country value. Value passed here for compatibility"""
        return 'resource__country' + self.FILTER_MODIFIER, value, 200

    def _title_query(self, value):
        """ Return query params for news filtered by title value. Value passed here for compatibility"""
        return 'title' + self.FILTER_MODIFIER, value, 200

    def _from_query(self, value):
        """ Return query params for news with pub_date greater than value."""
        date, status = self._extract_date(value)
        return 'date__gt', date, status

    def _until_query(self, value):
        """ Return query params for news with pub_date less than value."""
        date, status = self._extract_date(value)
        return 'date__lt', date, status

    def _extract_date(self, value):
        """ Parse date data from value. Passed value should be a string in ISO 8601 format (YYYY-MM-DD) """
        passed = value
        try:
            value = [int(val) for val in value.split('-')]
            return date(*value), 200
        except (ValueError, TypeError):
            return passed, 400


class NewsByFilterListView(NewsQueries, View):

    def _bad_request(self, bad_value, url_parameter):
        """ Returns appropriate response if requested parameters is invalid"""
        resp = {
            'status_code': 400,
            'status_name': 'Bad Request',
            'reason': f'"{bad_value}" - is not valid {url_parameter} to this request!',
        }
        return JsonResponse(resp)

    def get(self, request, request_type, value):
        """
        Get values passed in url and return filtered list of News object. Case is insensitive

        possible values for 'field_name' url parameter:
            'title' -  search news with given title (i.g. 'tittle=odessa')
            'category' - search news for given category name (i.g. 'category=sport')
            'country' - search news for given resource country name (i.g. 'country=Germany')
            'from' - search news from given date to current. This date should be in ISO 8601 format (YYYY-MM-DD)
                    (e.g. from=2018-11-09)
            'until' - search news from oldest date to given (e.g. until=2018-11-09)

        If you want specify more query options you should:
            1. add parameter name in 'FILTER_MAP' below
            2. bound added parameter with method which you need to implement in 'NewsQueries'
        """
        FILTER_MAP = {
            'title': self._title_query,
            'category': self._category_query,
            'country': self._country_query,
            'from': self._from_query,
            'until': self._until_query,
        }

        if request_type not in FILTER_MAP:
            return self._bad_request(request_type, 'request type')

        query, value, status_code = FILTER_MAP[request_type](value)

        if status_code != 200:
            return self._bad_request(value, 'value')

        context = {'news': News.objects.filter(**{query: value})}
        return render(request, 'news_aggregator/news_filter_list.html', context=context)


def documentation_view(request):
    if request.method == 'GET':
        return render(request, 'news_aggregator/docs.html')
