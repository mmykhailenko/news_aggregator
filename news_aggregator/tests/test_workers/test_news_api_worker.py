from django.test import TestCase
from news_aggregator.models import News
from news_aggregator.workers.serializers import NewsAPISerializer
from news_aggregator.workers.collectors import NewsAPICollector


class TestNewsAPIWorker(TestCase):
    """
        Binds work of collector and serializer
    """

    news_api_collector = NewsAPICollector()
    news_api_serializer = NewsAPISerializer()

    def test_is_data_collected_and_serialized(self):
        self.news_api_collector.collect()
        self.news_api_serializer.serialize(self.news_api_collector.news_storage,
                                           country=self.news_api_collector.QUERY_PARAMS['country'],
                                           lang=self.news_api_collector.QUERY_PARAMS['language'])
        self.assertTrue(News.objects.all())
