from time import sleep
from .collectors import NewsAPICollector
from .serializers import NewsAPISerializer


def news_api_worker_run():
    news_api_collector = NewsAPICollector()
    news_api_serializer = NewsAPISerializer()

    while True:
        news_api_collector.collect()
        news_api_serializer.serialize(news_api_collector.news_storage,
                                      country=news_api_collector.QUERY_PARAMS['country'],
                                      lang=news_api_collector.QUERY_PARAMS['language'])
        sleep(15)
