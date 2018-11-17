import requests
import schedule
import time
from urllib.parse import urlparse
from django.utils import timezone

from news_aggregator.workers.BaseWorkerAbstract import BaseWorkerAbstract
from news_aggregator.models import Category, News, Resource

class NewsApiWorker(BaseWorkerAbstract):
    BASE_URL = "https://newsapi.org"
    API_VERSION = "v2"
    API_KEY = "488c6cc7d5b04c3ea87b8d672152eeaf"


    def _process_data(self, raw_news):
        for news in raw_news:

            news_valid = self._validate_news(news)
            if not news_valid:
                continue

            news_source = self._serialize_source(news)
            self._serialize_news(news, news_source)


    def _validate_news(self, news):
        if None in news.values():
            return False

        return True


    def _serialize_source(self, news):
        news_source_url = urlparse(news['url'])
        source_name = news['source']['name'] or "{uri.netloc}".format(uri=news_source_url)
        source_country = self.country
        source_url = "{uri.scheme}://{uri.netloc}/".format(uri=news_source_url)
        news_source, _ = Resource.objects.get_or_create(name=source_name,
                                                        country=source_country,
                                                        resource_url=source_url)
        return news_source


    def _serialize_news(self, news, news_source):
        news_title = news['title']
        news_date = news['publishedAt']
        news_content = news['content']
        news_category, _ = Category.objects.get_or_create(name=self.category)
        News.objects.get_or_create(title=news_title,
                                   date=news_date,
                                   content=news_content,
                                   resource=news_source,
                                   category=news_category,
                                   )


class TopHeadlinesWorker(NewsApiWorker):

    def __init__(self, country, language=None):
        self.country = country
        self.language = language or "en"
        self.category = None
        self.last_update = timezone.now()


    def _url_construct(self):
        base_url = f"{self.BASE_URL}/{self.API_VERSION}/top-headlines?apiKey={self.API_KEY}"
        postfix_url = f"&country={self.country}&category={self.category}"

        return f"{base_url}{postfix_url}"


    def get_news(self):
        categories = (
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology"
        )

        # while True:
        for category in categories:
            self.category = category
            url = self._url_construct()
            print(f"{timezone.now()} - {url} - get top headlines.")

            with requests.Session() as session:
                response = session.get(url).json()
                self._process_data(response['articles'])
                self.last_update = timezone.now()


    def run_worker(self):
        schedule.every(60).seconds.do(self.get_news)

        while 1:
            schedule.run_pending()
            time.sleep(60)


class EverythingWorker(NewsApiWorker):

    def __init__(self, query, language=None):
        self.query = query
        self.language = language or "en"
        self.category = "everything"
        self.last_update = timezone.now()


    def _url_construct(self):
        base_url = f"{self.BASE_URL}/{self.API_VERSION}/top-everything?apiKey={self.API_KEY}"
        postfix_url = f"&q={self.query}&language={self.language}"

        return f"{base_url}{postfix_url}"


    def get_news(self):
        url = self._url_construct()
        print(f"{timezone.now()} - {url} - get all news.")

        with requests.Session() as session:
            response = session.get(url).json()
            self._process_data(response['articles'])
            self.last_update = timezone.now()


    def run_worker(self):
        schedule.every(60).seconds.do(self.get_news)

        while 1:
            schedule.run_pending()
            time.sleep(60)