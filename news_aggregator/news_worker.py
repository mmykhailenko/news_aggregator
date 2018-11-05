import requests
import time
import schedule
from django.utils import timezone

from news_aggregator.models import Category, News


class NewsWorker:

    def __init__(self, country, category, lang):
        self.country = country
        self.category = Category.objects.get_or_create(name=category)
        self.language = lang
        self.time_step = 10
        self.url_base = f'https://newsapi.org/v2/top-headlines?q={self.category[0]}&language={self.language}&apiKey=488c6cc7d5b04c3ea87b8d672152eeaf'
        self.data = dict()

    def get_news(self):

        with requests.Session() as session:
            response = session.get(self.url_base).json()
            self._serialize_news(response['articles'])
            print(f"Get news {timezone.now()}: {response}")

    def _serialize_news(self, raw_news):
        for n in raw_news:
            print(f"===\n\t{n['title']}\n===")
            News.objects.get_or_create(title=n['title'], date=n['publishedAt'], content=n['description'], category=self.category[0])


