from django.test import TestCase
from news_aggregator.workers.collectors import NewsAPICollector


class TestNewsAPICollector(TestCase):

    def setUp(self):
        self.collector = NewsAPICollector()

    def tearDown(self):
        del self.collector

    def test_is_constant_vars_valid(self):
        self.assertIsNone(self.collector._checklist())

    def test_put(self):
        """ Test is put add data to storage"""
        self.collector.put('category', {'articles': None})
        self.assertTrue(self.collector.news_storage)

    def test_is_data_collected(self):
        self.collector.collect()
        self.assertTrue(self.collector.news_storage)
