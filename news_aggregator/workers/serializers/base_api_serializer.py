from abc import abstractmethod
from news_aggregator.workers.worker_logger import WorkerLogger


class BaseAPISerializer:

    @abstractmethod
    def get(self, storage):
        """
        You should write own implementation for this method, according on type of storage for collected data you used
        in 'Collector' class for chosen API.

        Notice that you should extract data from storage. Otherwise you will stuck in infinite loop
        :param storage: Place where you store collected data
        :return: Data that you get from storage
        """

    def __init__(self):
        self.logger = WorkerLogger().get_logger('news_api_serializer')

    @abstractmethod
    def process_data(self, data, **kwargs):
        """
        You should write own implementation for this method. Here you will perform all actions on collected data.
        """

    def serialize(self, storage, **kwargs):
        """ Run 'self.process_data' for every object from 'storage' retrieved by 'self.get' """
        self.logger.info('Start processing raw data...\n')
        while storage:
            data = self.get(storage)
            self.process_data(data, **kwargs)
        self.logger.debug('All data handled.\n')
        self.logger.info(f'End of processing...\n{("-"*30)}\n')
