class APICollectorErrors(Exception):
    pass


class VariableNotDefinedError(APICollectorErrors):
    pass


class CollectorValueError(APICollectorErrors):
    pass
