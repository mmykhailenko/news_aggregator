import logging
from django.conf import settings


class WorkerLogger:

    LOGGER_CONFIGS = {
        'filename': 'worker_logs.txt',
        'filemode': 'a',
        'level': 10 if settings.DEBUG else 20,
        'format': '%(name)s: %(levelname)s: %(asctime)s: %(message)s',
        'datefmt': '%m/%d/%Y %I:%M:%S'
    }

    def get_logger(self, name):
        logging.basicConfig(**self.LOGGER_CONFIGS)
        return logging.getLogger(name=name)
