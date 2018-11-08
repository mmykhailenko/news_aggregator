class BaseWorkerAbstract:

    def _auth(self):
        raise NotImplementedError

    def _url_construct(self):
        raise NotImplementedError

    def _validate_data(self):
        raise NotImplementedError
    