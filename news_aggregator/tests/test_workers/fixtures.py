from news_aggregator.workers.collectors import BaseAPICollector


class CreateBaseAPICollector:
    """
        Create class with overwritten constant variables in context manager, and delete it in '__exit__'
    """

    def __init__(self, query_params=None, base_url=None, mqpn=None, mqpv=None):
        self.query_params = query_params
        self.base_url = base_url
        self.mqpn = mqpn
        self.mqpv = mqpv

    def __enter__(self):
        class CustomBaseAPICollector(BaseAPICollector):

            MUTABLE_QUERY_PARAM_NAME = self.mqpn
            MUTABLE_QUERY_PARAM_VALUES = self.mqpv
            QUERY_PARAMS = self.query_params
            BASE_URL = self.base_url

            def put(self, value, data):
                """ It's abstract method, should be overwritten"""
                pass

        return CustomBaseAPICollector()

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self
