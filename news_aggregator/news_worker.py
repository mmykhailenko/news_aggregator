from urllib.parse import urljoin, urlparse

import requests
import time
import schedule
from django.utils import timezone


from .models import Category, News, Resource

# TODO: make adapter and base worker class
class NewsWorker:

    BASE_URL = "https://newsapi.org/"
    API_VERSION = "v2/"
    API_TYPE = "everything"
    API_KEY = "488c6cc7d5b04c3ea87b8d672152eeaf"

    def __init__(self, country, category, lang):
        self.base_url = NewsWorker.BASE_URL
        self.country = country or "us"
        self.category = Category.objects.get_or_create(name=category)[0]
        self.language = lang
        self.time_step = 10
        self.url_base = self._url_create()
        self.data = dict()


    def _url_create(self):
        postfix_url = f'pageSize=100&q={self.category}&language={self.language}'
        # url = urljoin(self.base_url, self.API_VERSION, self.API_TYPE, postfix_url)
        url = f"https://newsapi.org/v2/everything?apiKey=488c6cc7d5b04c3ea87b8d672152eeaf&{postfix_url}"

        return url

    def get_news(self):

        with requests.Session() as session:
            response = session.get(self.url_base).json()
            self._serialize_news(response['articles'])

    def _serialize_news(self, raw_news):
        for n in raw_news:
            n_source_url = urlparse(n['url'])
            n_source = Resource.objects.get_or_create(name=n['source']['name'],
                                                      country=self.country,
                                                      resource_url='{uri.scheme}://{uri.netloc}/'.format(uri=n_source_url))[0]
            prep_news = News.objects.get_or_create(title=n['title'],
                                                   date=n['publishedAt'],
                                                   content=n['description'],
                                                   category=self.category,
                                                   res = n_source)[0]



# TODO: make scheduled workers