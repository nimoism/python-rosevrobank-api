from __future__ import absolute_import

import requests

from rosevrobank.backends.base.backend import BaseBackend, AuthBackendMixin
from rosevrobank.backends.rest.fields import MoneyField, DateTimeField, CardDateField, TimestampField
from rosevrobank.response import ErrorResponse, Response, HttpErrorResponse, ResponseData
from rosevrobank.exceptions import ResponseException


class RestBackend(AuthBackendMixin, BaseBackend):
    URL = 'https://paymentgate.ru/rebpayment/rest/'
    TEST_URL = 'https://test.paymentgate.ru/rebpayment/rest/'
    ACTION_REGISTER_ORDER = 'register'
    ACTION_PRE_AUTH_REGISTER_ORDER = 'registerPreAuth'
    ACTION_DEPOSIT = 'deposit'
    ACTION_REVERSE_ORDER = 'reverse'
    ACTION_REFUND = 'refund'
    ACTION_GET_ORDER_STATUS = 'getOrderStatus'
    ACTION_GET_EXTENDED_ORDER_STATUS = 'getOrderStatusExtended'
    ACTION_VERIFY_ENROLLMENT = 'verifyEnrollment'
    ACTION_PAYMENT_ORDER_BINDING = 'paymentOrderBinding'
    ACTION_UNBIND_CARD = 'unBindCard'
    ACTION_BIND_CARD = 'bindCard'
    ACTION_EXTEND_BINDING = 'extendBinding'
    ACTION_GET_BINDINGS = 'getBindings'
    ACTION_GET_LAST_ORDERS_FOR_MERCHANTS = 'getLastOrdersForMerchants'

    actions = (
        ACTION_REGISTER_ORDER,
        ACTION_PRE_AUTH_REGISTER_ORDER,
        ACTION_DEPOSIT,
        ACTION_REVERSE_ORDER,
        ACTION_REFUND,
        ACTION_GET_ORDER_STATUS,
        ACTION_GET_EXTENDED_ORDER_STATUS,
        ACTION_VERIFY_ENROLLMENT,
        ACTION_PAYMENT_ORDER_BINDING,
        ACTION_UNBIND_CARD,
        ACTION_BIND_CARD,
        ACTION_EXTEND_BINDING,
        ACTION_GET_BINDINGS,
        ACTION_GET_LAST_ORDERS_FOR_MERCHANTS
    )

    FIELDS = {
        ACTION_REGISTER_ORDER: {
            'amount': MoneyField(),
            'expiration_date': DateTimeField(),
        },
        ACTION_GET_ORDER_STATUS: {
            'amount': MoneyField(),
            'expiration': CardDateField(),
        },
        ACTION_GET_EXTENDED_ORDER_STATUS: {
            'amount': MoneyField(),
            'date': TimestampField(),
            'expiration': CardDateField(),
        }
    }

    def __init__(self, **kwargs):
        self.set_secure(kwargs.pop('user_name'), kwargs.pop('password'))
        self.test = kwargs.pop('test', False)
        super(RestBackend, self).__init__(**kwargs)

    def _get_action_url(self, action, test=None):
        if action not in self.actions:
            raise AttributeError("Action not found in action list")
        url = self.TEST_URL if self._is_test(test) else self.URL
        return url + action + '.do'

    def _get_params(self, raw_params):
        params = {}
        parameter_map_dict = dict(self.parameter_map)
        for raw_name, raw_value in raw_params.iteritems():
            param_name = parameter_map_dict[raw_name] if raw_name in parameter_map_dict else raw_name
            param_value = raw_value
            params[param_name] = param_value
        return params

    def _build_params(self, raw_data, action):
        params = {}
        parameter_map_reverse_dict = dict(self.parameter_map_reverse)
        for raw_name, raw_value in raw_data.iteritems():
            if raw_name in parameter_map_reverse_dict:
                param_name = parameter_map_reverse_dict[raw_name]
            else:
                param_name = raw_name
            field = self.FIELDS.get(action, {}).get(param_name)
            if field:
                raw_value = field.to_python(raw_value)
            if isinstance(raw_value, list):
                raw_value_list = list(raw_value)
                raw_value = []
                for sub_raw_data in raw_value_list:
                    raw_value.append(self._build_params(sub_raw_data, action))
            elif isinstance(raw_value, dict):
                raw_value = self._build_params(raw_value, action)
            params[param_name] = raw_value
        return ResponseData(params)

    def _process_response(self, http_response, action, raise_error=None):
        if http_response.status_code == 200:
            raw_data = http_response.json()
            if self.PARAM_ERROR_CODE in raw_data and int(raw_data[self.PARAM_ERROR_CODE]) != 0:
                response = ErrorResponse(raw_data[self.PARAM_ERROR_CODE], raw_data[self.PARAM_ERROR_MESSAGE])
            else:
                data = self._build_params(raw_data, action)
                response = Response(data.data)
        else:
            response = HttpErrorResponse(http_response)
        if self._should_raise_error(raise_error) and isinstance(response, ResponseException):
            raise response
        return response

    def _should_raise_error(self, raise_error=None):
        if raise_error is not None:
            return raise_error
        return self.raise_errors

    def _do_action(self, action, **kwargs):
        test = kwargs.pop('test', None)
        raise_errors = kwargs.pop('raise_errors', None)
        params = self._get_params(kwargs)
        return self.__do_action(action, params, raise_error=raise_errors, test=test)

    def __do_action(self, action, params, raise_error=None, test=None):
        self._append_secure(params)
        url = self._get_action_url(action, test=test)
        http_response = requests.get(url, params=params)
        return self._process_response(http_response, action, raise_error=raise_error)

    def _is_test(self, test):
        if test is not None:
            return test
        return self.test

    def register_order(self, **kwargs):
        return self._do_action(self.ACTION_REGISTER_ORDER, **kwargs)

    def reverse_order(self, **kwargs):
        return self._do_action(self.ACTION_REVERSE_ORDER, **kwargs)

    def refund(self, **kwargs):
        return self._do_action(self.ACTION_REFUND, **kwargs)

    def get_order_status(self, **kwargs):
        return self._do_action(self.ACTION_GET_ORDER_STATUS, **kwargs)

    def get_extended_order_status(self, **kwargs):
        return self._do_action(self.ACTION_GET_EXTENDED_ORDER_STATUS, **kwargs)

    def verify_enrolling(self, **kwargs):
        return self._do_action(self.ACTION_VERIFY_ENROLLMENT, **kwargs)

    def get_last_orders_for_merchants(self, **kwargs):
        return self._do_action(self.ACTION_GET_LAST_ORDERS_FOR_MERCHANTS, **kwargs)

    def pre_auth_register_order(self, **kwargs):
        return self._do_action(self.ACTION_PRE_AUTH_REGISTER_ORDER, **kwargs)

    def deposit(self, **kwargs):
        return self._do_action(self.ACTION_DEPOSIT, **kwargs)

    def payment_order_binding(self, **kwargs):
        return self._do_action(self.ACTION_PAYMENT_ORDER_BINDING, **kwargs)

    def unbind_card(self, **kwargs):
        return self._do_action(self.ACTION_UNBIND_CARD, **kwargs)

    def extend_binding(self, **kwargs):
        return self._do_action(self.ACTION_EXTEND_BINDING, **kwargs)

    def get_bindings(self, **kwargs):
        return self._do_action(self.ACTION_GET_BINDINGS, **kwargs)
