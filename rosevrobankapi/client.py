from rosevrobankapi.backends.base.backend import BaseBackend


class RosEvroBankClient(object):

    ORDER_STATUS_REGISTERED = 0
    ORDER_STATUS_PRE_AUTH_HOLD = 1
    ORDER_STATUS_AUTHORIZED = 2
    ORDER_STATUS_AUTH_CANCELLED = 3
    ORDER_STATUS_REFUNDED = 4
    ORDER_STATUS_ACS_AUTH_INITIATED = 5
    ORDER_STATUS_AUTH_REJECTED = 6

    AUTH_SUCCESS = 0
    AUTH_ERROR_UNKNOWN = 1
    AUTH_ERROR_REJECTED_BY_EMITTER = 2
    AUTH_ERROR_EMITTER_NO_ANSWERED = 3
    AUTH_ERROR_EMITTER = 4
    AUTH_ERROR_WRONG_AMOUNT = 5
    AUTH_ERROR_CARD_EXPIRED = 6
    AUTH_ERROR_ONLINE_PAYMENT_FORBIDDEN = 7
    AUTH_ERROR_WRONG_DATA_FORMAT = 8
    AUTH_ERROR_AMOUNT_GREATER_THAN_LIMIT = 10
    AUTH_ERROR_RECEIVED_ENDING_FOR_OVERDUE_PAYMENT = 11

    def __init__(self, **kwargs):
        backend = kwargs.get('backend')
        if not isinstance(backend, BaseBackend):
            raise AttributeError("Attribute 'backend' must be BaseBackend instance")
        self.backend = backend
        self.test = kwargs.get('test', False)

    def _prepare_action_params(self, kwargs):
        kwargs.setdefault('test', self.test)

    def register_order(self, order_number, amount, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'order_number': order_number,
            'amount': amount,
        })
        return self.backend.register_order(**kwargs)

    def reverse_order(self, order_id, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'order_id': order_id,
        })
        return self.backend.reverse_order(**kwargs)

    def refund(self, order_id, amount, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'order_id': order_id,
            'amount': amount,
        })
        return self.backend.refund(**kwargs)

    def get_order_status(self, order_id, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'order_id': order_id,
        })
        return self.backend.get_order_status(**kwargs)

    def get_extended_order_status(self, order_id=None, order_number=None, **kwargs):
        self._prepare_action_params(kwargs)
        if not order_id and not order_number:
            raise AttributeError('Parameters order_id or order_number must be passed')
        kwargs.update({
            'order_id': order_id,
            'order_number': order_number,
        })
        return self.backend.get_extended_order_status(**kwargs)

    def verify_enrolling(self, pan, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'pan': pan,
        })
        return self.backend.verify_enrolling(**kwargs)

    def get_last_orders_for_merchants(self, size, from_, to, transaction_states, merchants, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'size': size,
            'from': from_,
            'to': to,
            'transaction_states': transaction_states,
            'merchants': merchants,
        })
        return self.backend.get_last_orders_for_merchants(**kwargs)

    def pre_auth_register_order(self, order_number, amount, return_url, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'order_number': order_number,
            'amount': amount,
            'return_url': return_url,
        })
        return self.backend.pre_auth_register_order(**kwargs)

    def deposit(self, order_id, amount, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'order_id': order_id,
            'amount': amount,
        })
        return self.backend.deposit(**kwargs)

    def payment_order_binding(self, order_id, binding_id, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'md_order': order_id,
            'binding_id': binding_id,
        })
        return self.backend.payment_order_binding(**kwargs)

    def unbind_card(self, binding_id, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'binding_id': binding_id,
        })
        return self.backend.unbind_card(**kwargs)

    def extend_binding(self, binding_id, new_expiry, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'binding_id': binding_id,
            'new_expiry': new_expiry,
        })
        return self.backend.extend_binding(**kwargs)

    def get_bindings(self, client_id, **kwargs):
        self._prepare_action_params(kwargs)
        kwargs.update({
            'client_id': client_id
        })
        return self.backend.get_bindings(**kwargs)
