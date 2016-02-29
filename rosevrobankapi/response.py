from __future__ import unicode_literals

from rosevrobankapi.exceptions import ResponseException


class BaseResponse(object):
    pass


class BaseErrorResponse(BaseResponse, ResponseException):
    pass


class ApplicationErrorResponse(BaseErrorResponse):
    def __init__(self, code, message, data=None):
        self.message = message
        self.code = code
        self.data = data

    def __str__(self):
        return "{message} ({code})".format(message=self.message, code=self.code)


class HttpErrorResponse(BaseErrorResponse):
    def __init__(self, http_response):
        self.message = "Response was returned with HTTP code: %s" % http_response.status_code
        self.http_response = http_response

    def __str__(self):
        return self.message


class ResponseData(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item):
        return self.data.__contains__(item)

    def __len__(self):
        return self.data.__len__()


class Response(ResponseData, BaseResponse):
    pass
