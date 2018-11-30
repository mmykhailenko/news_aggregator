import logging

from django.apps import AppConfig
from django.db.utils import OperationalError


class NewsAggregatorConfig(AppConfig):
    name = 'news_aggregator'
    verbose_name = 'Worker'
    is_worker_running = False

    # def ready(self):
    #     try:
    #         news = self.get_model('news')
    #         news.objects.first()
    #     except OperationalError:
    #         logging.info('OperationalError exceptions in "news_aggregator/apps" suppressed')
    #     else:
    #         if not self.is_worker_running:
    #             self.is_worker_running = True
    #
    #             from .workers.worker_run import news_api_worker_run
    #
    #             news_api_worker_run()
