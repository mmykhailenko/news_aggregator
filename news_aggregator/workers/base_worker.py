import asyncio
import aiohttp
import logging


class APICollectorErrors(Exception):
    pass


class NotOverwrittenError(APICollectorErrors):
    pass


class BadValueError(APICollectorErrors):
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
         - When overriding '__init__' should call it's super()
    """

    LOGGER_CONFIGS = {}  # Should be dict

    # Parameter which will have different values
    MUTABLE_QUERY_PARAM_NAME = ''  # Should be str
    # Values for parameter above.
    MUTABLE_QUERY_PARAM_VALUES = []  # Should be iterable, not str

    # Other query parameters
    QUERY_PARAMS = {}  # Should be dict

    WORKER_REST_TIME = 0  # Should be int or float, and >= 0

    BASE_URL = ''  # Should be str

    def __init__(self, logger_name, forever=False):
        self.log_worker = self._get_logger(logger_name)
        self.forever = forever

    def _get_logger(self, name):
        logging.basicConfig(**self.LOGGER_CONFIGS)
        return logging.getLogger(name=name)

    def _is_overwritten_values_valid(self):
        # TODO: Add validators for other values
        validators = (
            self._validate_worker_rest_time(),
        )
        for result, var_name, message in validators:
            if not result:
                raise BadValueError(f'Wrong value for {var_name}! It should be {message}')

    def _validate_worker_rest_time(self):
        """ Returns: tuple: (bool value, 'variable name, 'what value is should be') """
        value = self.WORKER_REST_TIME
        return isinstance(value, (int, float)) and value >= 0, 'WORKER_REST_TIME', 'int or float, and >= 0'

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
        This method will run only after all data was collected and, if it process run in infinite loop,
        before collector's rest time countdown begins
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
        if self.MUTABLE_QUERY_PARAM_VALUES and self.MUTABLE_QUERY_PARAM_NAME:
            tasks = [asyncio.ensure_future(self._collect_data(value, **self.QUERY_PARAMS)) for
                     value in self.MUTABLE_QUERY_PARAM_VALUES]
        else:
            raise NotOverwrittenError("Your worker can't create tasks. You should overwrite "
                                      "'MUTABLE_QUERY_PARAM_NAME' and 'MUTABLE_QUERY_PARAM_VALUES' in your subclass")
        return tasks

    async def _scheduler(self):
        """ This method tie all parts together """
        self.log_worker.info('Create tasks...\n')
        tasks = self._create_tasks()
        await asyncio.wait(tasks)  # Run 'self._collect_news' for every task and waits until their finish
        self.process_data()  # Do nothing if subclasses don't override this
        self.log_worker.info(f'Loop is finished\n{("-" * 30)}')

    async def _run_forever(self):
        self.log_worker.info('Running forever...\n\n')
        while True:
            await self._scheduler()
            self.log_worker.info(f'Next loop starts after {self.WORKER_REST_TIME} seconds\n{("-" * 30)}')
            await asyncio.sleep(self.WORKER_REST_TIME)

    async def _run_once(self):
        self.log_worker.info('Running once...\n\n')
        await self._scheduler()

    def run(self):
        """ Starts infinite loop """
        self.log_worker.info('Validate variables values...')
        self._is_overwritten_values_valid()
        self.log_worker.info('Prepare event loops...')
        asyncio.set_event_loop(asyncio.new_event_loop())
        ioloop = asyncio.get_event_loop()
        try:
            if self.forever:
                asyncio.ensure_future(self._run_forever())
                ioloop.run_forever()
            else:
                ioloop.run_until_complete(self._run_once())
        except KeyboardInterrupt:
            pass
        finally:
            ioloop.close()
            self.log_worker.info('Worker stopped...\n')
