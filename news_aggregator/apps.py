from django.apps import AppConfig


class NewsAggregatorConfig(AppConfig):
    name = 'news_aggregator'

    def ready(self):
        from news_aggregator.workers.NewsApiWorker import TopHeadlinesWorker

        news_worker = TopHeadlinesWorker(country="us")
        news_worker.run_worker()