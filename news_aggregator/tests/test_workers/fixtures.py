import pytest

from news_aggregator.workers.collectors import BaseAPICollector, NewsAPICollector


@pytest.fixture(scope='session')
def invalid_base_api_collector_const():
    """
        Create class with incorrectly overwritten constant variables
    """
    class InvalidBaseAPICollector(BaseAPICollector):

        MUTABLE_QUERY_PARAM_NAME = None
        MUTABLE_QUERY_PARAM_VALUES = None
        QUERY_PARAMS = None
        BASE_URL = None

    return InvalidBaseAPICollector()
