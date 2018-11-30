from urllib.parse import urlparse
from django.utils import timezone
from .base_api_serializer import BaseAPISerializer
from news_aggregator.models import Category, News, Resource


class NewsAPISerializer(BaseAPISerializer):

    def get(self, storage):
        return storage.pop()

    def process_data(self, data, **kwargs):
        category, news = data.popitem()
        self.logger.debug(f'Processing: "{category}"...')
        news_category = self._serialize_category(category)
        for article in news:
            title, content, source_url, source_name, pub_date = self._extract_required_fields(article)
            if not self._have_required_fields(title, content, source_url, source_name):
                continue
            news_source = self._serialize_source(source_url, source_name, kwargs['country'])
            self._serialize_news(title, content, news_category, news_source, pub_date, kwargs['lang'])
        self.logger.debug(f'Processing finished for: "{category}"\n')

    def _extract_required_fields(self, article):
        title = article.get('title')
        content = article.get('content') or article.get('description')
        pub_date = article.get('publishedAt') or timezone.now()

        parsed_url = urlparse(article.get('url'))
        source_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_url)
        source_name = article.get('source').get('name') or "{uri.netloc}".format(uri=parsed_url)
        return title, content, source_url, source_name, pub_date

    def _have_required_fields(self, *fields):
        """ Check whether fields got values or not """
        return all(fields)

    def _serialize_source(self, source_url, source_name, country):
        news_source, _ = Resource.objects.get_or_create(name=source_name,
                                                        country=country,
                                                        resource_url=source_url)
        return news_source

    def _serialize_category(self, category):
        news_category, _ = Category.objects.get_or_create(name=category)
        return news_category

    def _serialize_news(self, title, content, news_category, news_source, pub_date, lang):
        News.objects.get_or_create(title=title,
                                   date=pub_date,
                                   content=content,
                                   resource=news_source,
                                   category=news_category,
                                   lang=lang)
