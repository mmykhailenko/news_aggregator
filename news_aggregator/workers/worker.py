from urllib.parse import urlparse
from django.conf import settings
from django.utils import timezone
from .base_worker import BaseAPICollector
from news_aggregator.models import Category, News, Resource


class NewsAPIWorker(BaseAPICollector):

    NEWS_API_KEY = 'aa1262221c4f4ca4b7e2491dbefbcecc'

    NEWS_API_URL = "https://newsapi.org/"
    API_VERSION = "v2/"
    API_REQUEST_TYPE = 'top-headlines/'

    BASE_URL = f'{NEWS_API_URL}{API_VERSION}{API_REQUEST_TYPE}'

    MUTABLE_QUERY_PARAM_NAME = 'category'
    MUTABLE_QUERY_PARAM_VALUES = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

    QUERY_PARAMS = {
        'language': 'en',
        'country': 'us',
        'apiKey': NEWS_API_KEY,
        'page_size': 20,
    }

    WORKER_REST_TIME = 5

    LOGGER_CONFIGS = {
        'filename': 'worker_logs.txt',
        'filemode': 'a',
        'level': 10 if settings.DEBUG else 20,
        'format': '%(name)s: %(levelname)s: %(asctime)s: %(message)s',
        'datefmt': '%m/%d/%Y %I:%M:%S'
    }

    news_storage = []

    def put(self, value, data):
        """ Overridden method """
        data = {value: data['articles']}
        self.news_storage.append(data)

    def process_data(self):
        self.log_worker.info('Raw news collected...\n')
        self.log_worker.info('Start processing raw news...\n')
        while self.news_storage:
            raw = self.news_storage.pop()
            category, news = raw.popitem()
            self.log_worker.debug(f'Processing: "{category}"...')
            news_category = self._serialize_category(category)
            for article in news:
                title, content, source_url, source_name, pub_date = self._extract_required_fields(article)
                if not self._have_required_fields(title, content, source_url, source_name):
                    continue
                news_source = self._serialize_source(source_url, source_name)
                self._serialize_news(title, content, news_category, news_source, pub_date)
            self.log_worker.debug(f'Processing finished for: "{category}"...\n')
        self.log_worker.debug('All articles handled.\n')
        self.log_worker.info('End of processing...')

    def _extract_required_fields(self, article):
        title = article['title']
        content = article['content'] or article['description']
        pub_date = article['publishedAt'] or timezone.now()

        parsed_url = urlparse(article['url'])
        source_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_url)
        source_name = article['source']['name'] or "{uri.netloc}".format(uri=parsed_url)
        return title, content, source_url, source_name, pub_date

    def _have_required_fields(self, *fields):
        """ Check whether fields got values or not """
        return all(fields)

    def _serialize_source(self, source_url, source_name):
        news_source, _ = Resource.objects.get_or_create(name=source_name,
                                                        country=self.QUERY_PARAMS['country'],
                                                        resource_url=source_url)
        return news_source

    def _serialize_category(self, category):
        news_category, _ = Category.objects.get_or_create(name=category)
        return news_category

    def _serialize_news(self, title, content, news_category, news_source, pub_date):
        News.objects.get_or_create(title=title,
                                   date=pub_date,
                                   content=content,
                                   resource=news_source,
                                   category=news_category,
                                   lang=self.QUERY_PARAMS['language'])
