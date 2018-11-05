import requests
import time
import schedule
from news_aggregator.models import News, Category

class NewsWorker:
    def __init__(self, country, category, lang):
        self.country = country
        self.category = Category.objects.get_or_create(name=category)
        self.language = lang
        self.time_step = 10
        self.url_base = f'https://newsapi.org/v2/top-headlines?q={self.category[0]}&language={self.language}&apiKey=488c6cc7d5b04c3ea87b8d672152eeaf'
        self.data = dict()

    def get_news(self):
        print(f"Get news {timezone.now()}")
        with requests.Session() as session:
            response = session.get(self.url_base).json()
            self.serialize_news(response['articles'])

    def serialize_news(self, raw_news):
        for n in raw_news:
            News.objects.get_or_create(title=n['title'], date=n['publishedAt'], content=n['description'], category=self.category[0])

w1 = NewsWorker("Ukraine", "sports", "en")

# Schedule data update every X seconds
schedule.every(30).minutes.do(w1.get_news())

# Main loop
while 1:
    schedule.run_pending()
    time.sleep(30)
