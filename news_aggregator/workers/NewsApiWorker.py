from urllib.parse import urlparse

import requests

from news_aggregator.workers.BaseWorkerAbstract import BaseWorkerAbstract
from news_aggregator.models import Category, News, Resource

class NewsApiWorker(BaseWorkerAbstract):

    BASE_URL = "https://newsapi.org"
    API_VERSION = "v2"
    API_KEY = "488c6cc7d5b04c3ea87b8d672152eeaf"

    def __init__(self, api_type, query, country, language, category, time_step):
        self.base_url = self.BASE_URL
        self.api_version = self.API_VERSION
        self.api_type = api_type or "top-headlines"
        self.api_key = self.API_KEY
        self.country = country or "us"
        self.query = query
        self.category, _ = Category.objects.get_or_create(name=category)
        self.language = language or "en"
        self.time_step = time_step or 10
        self.url = self._url_construct()


    def _url_construct(self):
        base_url = f"{self.base_url}/{self.api_version}/{self.api_type}?apiKey={self.api_key}"
        postfix_url = f"&q={self.query}"

        if self.api_type == "everything":
            postfix_url += f"&language={self.language}"
        elif self.api_type == "top-headlines":
            postfix_url += f"&country={self.country}"

        return f"{base_url}{postfix_url}"


    def get_news(self):

        with requests.Session() as session:
            response = session.get(self.url).json()
            self._process_data(response['articles'])


    def _process_data(self, raw_news):
        for news in raw_news:
            news_source = self._serialize_source(news)
            self._serialize_news(news, news_source)



    def _serialize_source(self, news):
        news_source_url = urlparse(news['url'])
        news_source, _ = Resource.objects.get_or_create(name=news['source']['name'],
                                                        country=self.country,
                                                        resource_url='{uri.scheme}://{uri.netloc}/'.format(uri=news_source_url))
        return news_source

    def _serialize_news(self, news, news_source):
        News.objects.get_or_create(title=news['title'],
                                   date=news['publishedAt'],
                                   content=news['description'],
                                   category=self.category,
                                   resource=news_source,
                                   lang=self.language)


# TODO: make scheduled workers