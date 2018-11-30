from .base_api_collector import BaseAPICollector


class NewsAPICollector(BaseAPICollector):

    NEWS_API_KEY = 'aa1262221c4f4ca4b7e2491dbefbcecc'

    NEWS_API_URL = "https://newsapi.org/"
    API_VERSION = "v2/"
    API_REQUEST_TYPE = 'top-headlines/'

    BASE_URL = f'{NEWS_API_URL}{API_VERSION}{API_REQUEST_TYPE}'

    MUTABLE_QUERY_PARAM_NAME = 'category'
    MUTABLE_QUERY_PARAM_VALUES = ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')

    QUERY_PARAMS = {
        'language': 'en',
        'country': 'us',
        'apiKey': NEWS_API_KEY,
        'page_size': 20,
    }

    def __init__(self):
        super().__init__()
        self.news_storage = []

    def put(self, value, data):
        """ Mark collected json data with name of category and put in the storage """
        data = {value: data.get('articles')}
        self.news_storage.append(data)
        self.logger.debug(f'Json response for {value} added in storage\n')
