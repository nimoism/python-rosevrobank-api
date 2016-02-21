from rosevrobankapi.exceptions import ResponseException


class BaseResponse(object):
    pass


class BaseErrorResponse(BaseResponse, ResponseException):
    pass


class ErrorResponse(BaseErrorResponse):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class HttpErrorResponse(BaseErrorResponse):
    def __init__(self, http_response):
        self.message = "Response was returned with HTTP code: %s" % http_response.status_code
        self.http_response = http_response


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


class Response(ResponseData, BaseResponse):
    pass
