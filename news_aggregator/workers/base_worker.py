import asyncio
import aiohttp
import logging


class APICollectorErrors(Exception):
    pass


class NothingToRequestError(APICollectorErrors):
    pass


class BaseAPICollector:
    """
    Implement asynchronous request operations

    subclasses TO DO's:
         - All subclasses should overwrite variables below.
         - Write own implementation for interactions with containers: queue/deque/list/dict/whatever. For this they
         should create container instance on class or object level and override 'put' method.
         - Subclasses can safely get access to collected data when overriding 'process_data' method.
         - Subclasses should call method 'run' to work
    """

    LOGGER_CONFIGS = {}

    # Parameter which will have different values
    MUTABLE_QUERY_PARAM_NAME = ''
    # Values for parameter above
    MUTABLE_QUERY_PARAM_VALUES = []

    # Other query parameters
    QUERY_PARAMS = {}

    WORKER_REST_TIME = 0

    BASE_URL = ''

    def __init__(self, logger_name):
        self.log_worker = self.get_logger(logger_name)

    def get_logger(self, name):
        logging.basicConfig(**self.LOGGER_CONFIGS)
        return logging.getLogger(name=name)

    def put(self, value, data):
        """
        You should write own implementation for this method, according on type of storage for collected data you will
        use. Also you can perform here various actions on your data before actual put

        :param value: query value associated with this data for distinguish.(It comes from 'MUTABLE_QUERY_PARAM_VALUES')
        :param data: collected json data from request
        """
        raise NotImplemented('You should write implementation! Otherwise your data is stored nowhere')

    def process_data(self):
        """
        In this method you can safely get data from container

        You should write own implementation for this method, if you want, according on actions, you want to perform on
        collected data.
        This method will run only after all data was collected and before collector's rest time countdown begins
        """
        pass

    async def _collect_data(self, value, **query_params):
        """ Sends requests and collect json response in container """
        # update static query params with changeable value
        query_params.update({self.MUTABLE_QUERY_PARAM_NAME: value})

        # disable ssl validation by creating custom Connector instance
        connector = aiohttp.TCPConnector(verify_ssl=False)
        try:
            self.log_worker.debug(f'Async request for "{value}" sending...')
            async with aiohttp.request('GET', self.BASE_URL, params=query_params, connector=connector) as resp:
                self.log_worker.info(f'Request status:{resp.status} received for "{value}" category')
                if resp.status == 200:
                    data = await resp.json()
                    self.put(value, data)
                else:
                    self.log_worker.error(f'Request status code: {resp.status}')
        except aiohttp.client_exceptions.ClientError as ex:
            self.log_worker.error(f'Exception: {ex}')
        finally:
            connector.close()

    def _create_tasks(self):
        """ Create tasks for asynchronous request """
        tasks = None
        if self.MUTABLE_QUERY_PARAM_VALUES:
            tasks = [asyncio.ensure_future(self._collect_data(value, **self.QUERY_PARAMS)) for
                     value in self.MUTABLE_QUERY_PARAM_VALUES]
        if not tasks:
            raise NothingToRequestError("Your worker can't create tasks. Did you override 'ITERABLE_QUERY_PARAM'?")
        return tasks

    async def _scheduler(self):
        """ This method tie all parts together and run it in infinite loop """
        self.log_worker.info('Running...\n\n')
        while True:
            self.log_worker.info('Create tasks...\n')
            tasks = self._create_tasks()
            await asyncio.wait(tasks)  # Run 'self._collect_news' for every task and waits until their finish
            self.process_data()  # Do nothing if subclasses don't override this
            self.log_worker.info(f'Loop is finished\n{("-" * 30)}')
            self.log_worker.info(f'Next loop starts after {self.WORKER_REST_TIME} seconds\n{("-" * 30)}')
            await asyncio.sleep(self.WORKER_REST_TIME)

    def run(self):
        """ Starts infinite loop """
        self.log_worker.info('Prepare event loops...')
        asyncio.set_event_loop(asyncio.new_event_loop())
        ioloop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self._scheduler())
            ioloop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            ioloop.close()
            self.log_worker.info('Worker stopped...')
