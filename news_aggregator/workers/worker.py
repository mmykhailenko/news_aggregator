import asyncio
import aiohttp

from urllib.parse import urlparse
from django.utils import timezone
from .worker_settings import (
    log_worker,
    NEWS_API_URL,
    QUERY_PARAMS,
    ITERABLE_QUERY_PARAM,
    WORKER_REST_TIME
)
from news_aggregator.models import Category, News, Resource


class NewsAPICollector:

    raw_news = []

    async def _collect_news(self, category, **query_params):
        query_params.update({'category': category})
        # disable ssl validation by creating custom Connector instance
        connector = aiohttp.TCPConnector(verify_ssl=False)
        try:
            log_worker.debug(f'Async request for "{category}" sending...')
            async with aiohttp.request('GET', NEWS_API_URL, params=query_params, connector=connector) as resp:
                log_worker.info(f'Request status:{resp.status} received for "{category}" category')
                data = await resp.json()
                if resp.status == 200:
                    # Add 'category' mark and put collected data in 'self.raw_news' for further processing
                    collected = {category: data['articles']}
                    self.raw_news.append(collected)
                else:
                    log_worker.error(f'Request status code: {resp.status}, message: {data["message"]}')
        except aiohttp.client_exceptions.ClientError as ex:
            log_worker.error(f'Exception: {ex}')
        finally:
            connector.close()

    async def _scheduler(self):
        log_worker.info('\nRunning...\n\n')
        while True:
            log_worker.info('Create tasks...\n')
            # Make tasks for every category
            tasks = [asyncio.ensure_future(self._collect_news(category, **QUERY_PARAMS)) for category in ITERABLE_QUERY_PARAM]
            # Run 'self._collect_news' for every CATEGORIES and waits until their finish
            await asyncio.wait(tasks)
            log_worker.info('Raw news collected...\n')
            log_worker.info('Start processing raw news...\n')
            self._process_data()
            log_worker.info('End of processing...')
            log_worker.info(f'Loop is finished\n{"-" * 30)}')
            log_worker.info(f'Next loop starts after {WORKER_REST_TIME} seconds\n{"-" * 30}')
            await asyncio.sleep(WORKER_REST_TIME)

    def _process_data(self):
        while self.raw_news:
            raw = self.raw_news.pop()
            category, news = raw.popitem()
            log_worker.debug(f'Processing: "{category}"...')
            news_category = self._serialize_category(category)
            for article in news:
                title, content, source_url, source_name, pub_date = self._extract_required_fields(article)
                if not self._have_required_fields(title, content, source_url, source_name):
                    continue
                news_source = self._serialize_source(source_url, source_name)
                self._serialize_news(title, content, news_category, news_source, pub_date)
            log_worker.debug(f'Processing finished for: "{category}"...\n')
        log_worker.debug('All articles handled.\n')

    def _extract_required_fields(self, article):
        title = article['title']
        content = article['content'] or article['description']
        pub_date = article['publishedAt'] or timezone.now()

        parsed_url = urlparse(article['url'])
        source_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_url)
        source_name = article['source']['name'] or "{uri.netloc}".format(uri=parsed_url)
        return title, content, source_url, source_name, pub_date

    def _have_required_fields(self, *fields):
        return all(fields)

    def _serialize_source(self, source_url, source_name):
        news_source, _ = Resource.objects.get_or_create(name=source_name,
                                                        country=QUERY_PARAMS['country'],
                                                        resource_url=source_url)
        return news_source

    def _serialize_category(self, category):
        news_category, _ = Category.objects.get_or_create(name=category)
        return news_category

    def _serialize_news(self, title, content, news_category, news_source, pub_date):
        News.objects.get_or_create(title=title,
                                   date=pub_date,
                                   content=content,
                                   resource=news_source,
                                   category=news_category,
                                   lang=QUERY_PARAMS['language'])

    def run(self):
        log_worker.info('Prepare event loops...')
        asyncio.set_event_loop(asyncio.new_event_loop())
        ioloop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self._scheduler())
            ioloop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            ioloop.close()
            log_worker.info('Worker stopped...')
