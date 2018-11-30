import requests

from abc import ABCMeta, abstractmethod
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from news_aggregator.workers.worker_logger import WorkerLogger
from .api_collector_exceptions import CollectorValueError


class BaseAPICollector(metaclass=ABCMeta):
    """
    Implement API request operations

    subclasses TO DO's:
         - Write own implementation for interactions with containers: queue/deque/list/dict/whatever. For this they
         should create container instance on class or object level and override 'put' method.
         - Subclasses should call method 'collect' to work
         - When overriding '__init__' should call it's super()
    """

    # Parameter which will have different values
    MUTABLE_QUERY_PARAM_NAME = ''  # Should be str

    # Values for parameter above.
    MUTABLE_QUERY_PARAM_VALUES = ()  # Should be list or tuple like object

    # Other query parameters
    QUERY_PARAMS = {}  # Should be dict

    BASE_URL = ''  # Should be str

    def __init__(self):
        self.logger = WorkerLogger().get_logger(self.__class__.__name__)  # Logger get name of instance class

    def collect(self):
        self.logger.info('Performing checks for class level variables...')
        self._checklist()

        self.logger.info('Start collecting...\n')
        self._collect_data()
        self.logger.info('All data collected...\n')

    @abstractmethod
    def put(self, value, data):
        """
        You should write own implementation for this method, according on type of storage for collected data you will
        use. Also you can perform here various actions on your data before actual put

        :param value: query value associated with this data for distinguish.(It comes from 'MUTABLE_QUERY_PARAM_VALUES')
        :param data: collected json data from request
        """

    def _collect_data(self):
        """ Sends requests and collect json response in container """
        for value in self.MUTABLE_QUERY_PARAM_VALUES:
            query_params = {self.MUTABLE_QUERY_PARAM_NAME: value, **self.QUERY_PARAMS}
            self.logger.info(f'Sending request for {value}...')

            resp = requests.get(self.BASE_URL, params=query_params)

            if resp.status_code == 200:
                self.logger.debug(f'Request status for {value} is {resp.status_code}')
                data = resp.json()
                self.put(value, data)
            else:
                self.logger.info(f'Request status code for "{value}" is: {resp.status_code}')

    def _checklist(self):
        self._is_base_url_valid()
        self._is_query_params_valid()
        self._is_mutable_query_param_name_valid()
        self._is_mutable_query_param_values_valid()

    def _is_base_url_valid(self):
        validator = URLValidator()
        url = self.BASE_URL

        if not isinstance(url, str):
            message = f'"BASE_URL": ({url}) should be string'
            self.logger.error(message)
            raise CollectorValueError(message)

        try:
            validator(url)
        except ValidationError:
            message = f'"BASE_URL": ({url}) is not valid.'
            self.logger.error(message)
            raise CollectorValueError(message)

    def _is_query_params_valid(self):
        if not isinstance(self.QUERY_PARAMS, dict):
            message = f'"QUERY_PARAMS" should be a dict instance'
            self.logger.error(message)
            raise CollectorValueError(f'"QUERY_PARAMS" should be a dict instance')

    def _is_mutable_query_param_name_valid(self):
        mqpn = self.MUTABLE_QUERY_PARAM_NAME
        if not isinstance(mqpn, str) or not mqpn:
            message = f'"MUTABLE_QUERY_PARAM_NAME" should be a non empty string'
            self.logger.error(message)
            raise CollectorValueError(message)

    def _is_mutable_query_param_values_valid(self):
        mqpw = self.MUTABLE_QUERY_PARAM_VALUES

        if not isinstance(mqpw, (tuple, list)) or not mqpw:
            message = "MUTABLE_QUERY_PARAM_VALUES should be a non empty tuple or list"
            self.logger.error(message)
            raise CollectorValueError(message)
