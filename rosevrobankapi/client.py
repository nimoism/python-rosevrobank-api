from logging import getLogger

from rosevrobankapi.backends.base.backend import BaseBackend
from rosevrobankapi.response import BaseErrorResponse


logger = getLogger(__name__)


class RosEvroBankClient(object):

    ORDER_STATUS_REGISTERED = 0
    ORDER_STATUS_PRE_AUTH_HOLD = 1
    ORDER_STATUS_AUTHORIZED = 2
    ORDER_STATUS_AUTH_CANCELLED = 3
    ORDER_STATUS_REFUNDED = 4
    ORDER_STATUS_ACS_AUTH_INITIATED = 5
    ORDER_STATUS_AUTH_REJECTED = 6

    def __init__(self, **kwargs):
        backend = kwargs.get('backend')
        if not isinstance(backend, BaseBackend):
            raise AttributeError("Attribute 'backend' must be BaseBackend instance")
        self.backend = backend

    def _call_backend(self, method, **kwargs):
        """
        :param method: method to call
        :type method: func
        :param kwargs:
        :return: rosevrobankapi.response.Response
        """
        try:
            response = method(**kwargs)
        except BaseErrorResponse as e:
            logger.exception(e, extra={'backend': self.backend.name, 'method': method.__name__})
            raise
        return response

    def register_order(self, order_number, amount, return_url, **kwargs):
        kwargs.update({
            'order_number': order_number,
            'amount': amount,
            'return_url': return_url,
        })
        return self._call_backend(self.backend.register_order, **kwargs)

    def reverse_order(self, order_id, **kwargs):
        kwargs.update({
            'order_id': order_id,
        })
        return self._call_backend(self.backend.reverse_order, **kwargs)

    def refund(self, order_id, amount, **kwargs):
        kwargs.update({
            'order_id': order_id,
            'amount': amount,
        })
        return self._call_backend(self.backend.refund, **kwargs)

    def get_order_status(self, order_id, **kwargs):
        kwargs.update({
            'order_id': order_id,
        })
        return self._call_backend(self.backend.get_order_status, **kwargs)

    def get_extended_order_status(self, order_id=None, order_number=None, **kwargs):
        if not order_id and not order_number:
            raise AttributeError('Parameters order_id or order_number must be passed')
        kwargs.update({
            'order_id': order_id,
            'order_number': order_number,
        })
        return self._call_backend(self.backend.get_extended_order_status, **kwargs)

    def verify_enrolling(self, pan, **kwargs):
        kwargs.update({
            'pan': pan,
        })
        return self._call_backend(self.backend.verify_enrolling, **kwargs)

    def get_last_orders_for_merchants(self, size, from_, to, transaction_states, merchants, **kwargs):
        kwargs.update({
            'size': size,
            'from': from_,
            'to': to,
            'transaction_states': transaction_states,
            'merchants': merchants,
        })
        return self._call_backend(self.backend.get_last_orders_for_merchants, **kwargs)

    def pre_auth_register_order(self, order_number, amount, return_url, **kwargs):
        kwargs.update({
            'order_number': order_number,
            'amount': amount,
            'return_url': return_url,
        })
        return self._call_backend(self.backend.pre_auth_register_order, **kwargs)

    def deposit(self, order_id, amount, **kwargs):
        kwargs.update({
            'order_id': order_id,
            'amount': amount,
        })
        return self._call_backend(self.backend.deposit, **kwargs)

    def payment_order_binding(self, order_id, binding_id, **kwargs):
        kwargs.update({
            'md_order': order_id,
            'binding_id': binding_id,
        })
        return self._call_backend(self.backend.payment_order_binding, **kwargs)

    def unbind_card(self, binding_id, **kwargs):
        kwargs.update({
            'binding_id': binding_id,
        })
        return self._call_backend(self.backend.unbind_card, **kwargs)

    def extend_binding(self, binding_id, new_expiry, **kwargs):
        kwargs.update({
            'binding_id': binding_id,
            'new_expiry': new_expiry,
        })
        return self._call_backend(self.backend.extend_binding, **kwargs)

    def get_bindings(self, client_id, **kwargs):
        kwargs.update({
            'client_id': client_id
        })
        return self._call_backend(self.backend.get_bindings, **kwargs)
