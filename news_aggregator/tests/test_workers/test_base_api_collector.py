from .fixtures import CreateBaseAPICollector
from django.test import TestCase
from news_aggregator.workers.collectors import CollectorValueError


class TestBaseAPICollector(TestCase):

    # ------------ Test '_is_base_url_valid' method --------------

    def test_empty_base_url(self):
        with CreateBaseAPICollector(base_url='') as collector:
            self.assertRaises(CollectorValueError, collector._is_base_url_valid)

    def test_invalid_base_url_value(self):
        with CreateBaseAPICollector(base_url='42') as collector:
            self.assertRaises(CollectorValueError, collector._is_base_url_valid)

    def test_invalid_base_url_type(self):
        with CreateBaseAPICollector(base_url=42) as collector:
            self.assertRaises(CollectorValueError, collector._is_base_url_valid)

    def test_valid_base_url(self):
        with CreateBaseAPICollector(base_url='https://www.python.org/') as collector:
            self.assertIsNone(collector._is_base_url_valid())

    # ------------ Test '_is_query_params_valid' method --------------

    def test_empty_query_params(self):
        with CreateBaseAPICollector(query_params={}) as collector:
            self.assertIsNone(collector._is_query_params_valid())

    def test_valid_query_params(self):
        with CreateBaseAPICollector(query_params={'language': 'en', 'country': 'us'}) as collector:
            self.assertIsNone(collector._is_query_params_valid())

    def test_invalid_query_params_type(self):
        with CreateBaseAPICollector(query_params=()) as collector:
            self.assertRaises(CollectorValueError, collector._is_query_params_valid)

    # ------------ Test '_is_mutable_query_param_name_valid' method --------------

    def test_invalid_mutable_query_param_name_type(self):
        with CreateBaseAPICollector(mqpn=42) as collector:
            self.assertRaises(CollectorValueError, collector._is_mutable_query_param_name_valid)

    def test_empty_mutable_query_param_name(self):
        with CreateBaseAPICollector(mqpn='') as collector:
            self.assertRaises(CollectorValueError, collector._is_mutable_query_param_name_valid)

    def test_valid_mutable_query_param_name(self):
        with CreateBaseAPICollector(mqpn='category') as collector:
            self.assertIsNone(collector._is_mutable_query_param_name_valid())

    # ------------ Test '_is_mutable_query_param_values_valid' method --------------

    def test_valid_list_mutable_query_param_values(self):
        with CreateBaseAPICollector(mqpv=['test', 'test']) as collector:
            self.assertIsNone(collector._is_mutable_query_param_values_valid())

    def test_empty_list_mutable_query_param_values(self):
        with CreateBaseAPICollector(mqpv=[]) as collector:
            self.assertRaises(CollectorValueError, collector._is_mutable_query_param_values_valid)

    def test_valid_tuple_mutable_query_param_values(self):
        with CreateBaseAPICollector(mqpv=('test', 'test')) as collector:
            self.assertIsNone(collector._is_mutable_query_param_values_valid())

    def test_empty_tuple_mutable_query_param_values(self):
        with CreateBaseAPICollector(mqpv=()) as collector:
            self.assertRaises(CollectorValueError, collector._is_mutable_query_param_values_valid)
