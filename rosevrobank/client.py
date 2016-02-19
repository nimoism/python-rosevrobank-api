from rosevrobank.backends.base.backend import BaseBackend


class RosEvroBankClient(object):
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
