from urllib.parse import urljoin, urlparse

import requests
import time
import schedule
from django.utils import timezone


from .models import Category, News, Resource

# TODO: make adapter and base worker class
class BaseWorker:

    def _auth(self):
        raise NotImplementedError

    def _url_construct(self):
        raise NotImplementedError

    def _validate_data(self):
        raise NotImplementedError

class NewsApiWorker(BaseWorker):

    BASE_URL = "https://newsapi.org"
    API_VERSION = "v2"
    API_TYPE = "top-headers"
    API_KEY = "488c6cc7d5b04c3ea87b8d672152eeaf"

    def __init__(self, api_type, api_key, query, country, category, language, time_step):
        self.base_url = self.BASE_URL
        self.api_version = self.API_VERSION
        self.api_type = api_type or "top-headers"
        self.api_key = api_key
        self.country = country or "ua"
        self.query = query
        self.category, _ = Category.objects.get_or_create(name=category)
        self.language = language or "uk"
        self.time_step = time_step or 10
        self.url = self._url_create()
        self.data = dict()


    def _url_create(self):
        base_url = f"{self.base_url}/{self.api_version}/{self.api_type}?apiKey={self.api_key}"
        postfix_url = f"&q={self.query}"

        if self.api_type == "everything":
            postfix_url += f"language={self.language}"
        elif self.api_type == "top-headers":
            postfix_url += f"country={self.country}"

        return f"{base_url}{postfix_url}"

    def get_news(self):

        with requests.Session() as session:
            response = session.get(self.url).json()
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



# class WorkerResponse:
#     def __init__(self):
#         self.title
#         self.url
#         self.content

# TODO: make scheduled workers