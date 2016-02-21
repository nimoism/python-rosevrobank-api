class RosEvroBankException(Exception):
    pass


class ImproperlyConfigured(RosEvroBankException):
    pass


class ResponseException(RosEvroBankException):
    pass
