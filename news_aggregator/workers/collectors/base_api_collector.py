import requests

from abc import abstractmethod
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from news_aggregator.workers.worker_logger import WorkerLogger
from .api_collector_exceptions import CollectorValueError, VariableNotDefinedError


class BaseAPICollector:
    """
    Implement API request operations

    subclasses TO DO's:
         - Write own implementation for interactions with containers: queue/deque/list/dict/whatever. For this they
         should create container instance on class or object level and override 'put' method.
         - Subclasses should call method 'collect' to work
         - When overriding '__init__' should call it's super()

         - Difine following variables:

            # Parameter which will have different values
            MUTABLE_QUERY_PARAM_NAME ---  # Should be str

            # Values for parameter above.
            MUTABLE_QUERY_PARAM_VALUES ---  # Should be iterable, not str

            # Other query parameters
            QUERY_PARAMS ---  # Should be dict

            BASE_URL ---  # Should be str
    """
    def __init__(self):
        self.logger = WorkerLogger().get_logger('news_api_collector')

    def _is_variables_created(self):
        try:
            self.MUTABLE_QUERY_PARAM_VALUES
            self.MUTABLE_QUERY_PARAM_NAME
            self.QUERY_PARAMS
            self.BASE_URL
        except AttributeError as ex:
            message = f"You didn't define variable in your subclass: {ex}"
            self.logger.error(message)
            raise VariableNotDefinedError(message)

    def _is_base_url_valid(self):
        val = URLValidator()
        url = self.BASE_URL
        if not url:
            raise CollectorValueError('"BASE_URL" cannot be empty')
        try:
            val(url)
        except ValidationError:
            message = f'"BASE_URL": ({url}) is not valid'
            self.logger.error(message)
            raise CollectorValueError(message)
        except AttributeError:
            message = f'"BASE_URL" should be a string'
            self.logger.error(message)
            raise CollectorValueError(message)

    def _is_query_params_valid(self):
        if not isinstance(self.QUERY_PARAMS, dict):
            raise CollectorValueError(f'"QUERY_PARAMS" should be a dict instance')

    def _is_mutable_query_param_name_valid(self):
        mqpn = self.MUTABLE_QUERY_PARAM_NAME
        if not isinstance(mqpn, str) or not mqpn:
            raise CollectorValueError(f'"MUTABLE_QUERY_PARAM_NAME" should be a non empty string')

    def _is_mutable_query_param_values_valid(self):
        mqpw = self.MUTABLE_QUERY_PARAM_VALUES
        try:
            getattr(mqpw, '__iter__')
        except AttributeError:
            raise CollectorValueError('MUTABLE_QUERY_PARAM_VALUES should be an iterable object, except dict instances')
        if isinstance(mqpw, dict):
            raise CollectorValueError("MUTABLE_QUERY_PARAM_VALUES attribute can't be dict")
        if not mqpw:
            raise CollectorValueError('MUTABLE_QUERY_PARAM_VALUES cannot be empty')
        for param in mqpw:
            if not isinstance(param, str) or not param:
                message = f'"{param}" isn\'t valid value for request. It should be a non empty string'
                self.logger.error(message)
                raise CollectorValueError(message)

    def _checklist(self):
        self._is_variables_created()
        self._is_base_url_valid()
        self._is_query_params_valid()
        self._is_mutable_query_param_name_valid()
        self._is_mutable_query_param_values_valid()

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

    def collect(self):
        self.logger.info('Performing checks for class level variables...')
        self._checklist()
        self.logger.info('Start collecting...\n')
        self._collect_data()
        self.logger.info('All data collected...\n')

