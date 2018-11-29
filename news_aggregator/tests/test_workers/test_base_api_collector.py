import pytest
from .fixtures import invalid_base_api_collector_const
from news_aggregator.workers.collectors import CollectorValueError
from django.test import TestCase


class TestBaseAPICollector(TestCase):

    @pytest.fixture(autouse=True)
    def set_up(self, invalid_base_api_collector_const):
        self._invalid_collector = invalid_base_api_collector_const

    def test_is_base_url_valid(self):
        with pytest.raises(CollectorValueError):
            self._invalid_collector._is_base_url_valid()

    def test_is_query_params_valid(self):
        with pytest.raises(CollectorValueError):
            self._invalid_collector._is_query_params_valid()

    def test_is_mutable_query_param_name_valid(self):
        with pytest.raises(CollectorValueError):
            self._invalid_collector._is_mutable_query_param_name_valid()

    def test_is_mutable_query_param_values_valid(self):
        with pytest.raises(CollectorValueError):
            self._invalid_collector._is_mutable_query_param_values_valid()
