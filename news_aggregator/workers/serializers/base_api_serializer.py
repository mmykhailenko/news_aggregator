from abc import ABCMeta, abstractmethod
from news_aggregator.workers.worker_logger import WorkerLogger


class BaseAPISerializer(metaclass=ABCMeta):
    """
    Implement interactions with defined collector's class data storage for chosen API.

    subclasses TO DO's:
         - Write own implementation for interactions with containers: queue/deque/list/dict/whatever. For this they
         should override 'get' method.
         - Subclasses should call method 'serialize' to start processing
         - When overriding '__init__' should call it's super()
    """

    def __init__(self):
        self.logger = WorkerLogger().get_logger(self.__class__.__name__)  # Logger get name of instance class

    def serialize(self, storage, **kwargs):
        """ Run 'self.process_data' for every object from 'storage' retrieved by 'self.get' """
        self.logger.info('Start processing raw data...\n')
        while storage:
            data = self.get(storage)
            self.process_data(data, **kwargs)
        self.logger.debug('All data handled.\n')
        self.logger.info(f'End of processing...\n{("-"*30)}\n')

    @abstractmethod
    def get(self, storage):
        """
        You should write own implementation for this method, according on type of storage for collected data you used
        in 'Collector' class for chosen API.

        Notice that you should extract data from storage. Otherwise you will stuck in infinite loop
        :param storage: Place where you store collected data
        :return: Data that you get from storage
        """

    @abstractmethod
    def process_data(self, data, **kwargs):
        """
        You should write own implementation for this method. Here you will perform all actions on collected data.
        """
