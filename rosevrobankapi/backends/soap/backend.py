from rosevrobankapi.backends.base.backend import BaseBackend


class SoapBackend(BaseBackend):
    name = 'soap'

    def __init__(self, **kwargs):
        raise NotImplementedError()
