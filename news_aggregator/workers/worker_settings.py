import logging


NEWS_API_KEY = 'aa1262221c4f4ca4b7e2491dbefbcecc'

BASE_URL = "https://newsapi.org/"
API_VERSION = "v2/"
API_REQUEST_TYPE = 'top-headlines/'

NEWS_API_URL = f'{BASE_URL}{API_VERSION}{API_REQUEST_TYPE}'

# Only this categories provided by news api.
CATEGORIES = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

QUERY_PARAMS = {
    'language': 'en',
    'country': 'us',
    'apiKey': NEWS_API_KEY,
    'page_size': 20,
}

WORKER_REST_TIME = 60  # in seconds

logging.basicConfig(
    filename='worker_logs.txt',
    filemode='a',
    level=logging.DEBUG,
    format='%(name)s: %(levelname)s: %(asctime)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S'
)

log_worker = logging.getLogger('log_worker')
