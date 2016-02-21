from rosevrobankapi.backends.base.backend import BaseBackend
from rosevrobankapi.response import Response


class DummyBackend(BaseBackend):
    name = 'dummy'

    def _do_action(self, **kwargs):
        response_data = kwargs.get('response_data', {})
        return Response(response_data)

    def pre_auth_register_order(self, **kwargs):
        return self._do_action(**kwargs)

    def get_order_status(self, **kwargs):
        return self._do_action(**kwargs)

    def refund(self, **kwargs):
        return self._do_action(**kwargs)

    def verify_enrolling(self, **kwargs):
        return self._do_action(**kwargs)

    def payment_order_binding(self, **kwargs):
        return self._do_action(**kwargs)

    def extend_binding(self, **kwargs):
        return self._do_action(**kwargs)

    def deposit(self, **kwargs):
        return self._do_action(**kwargs)

    def unbind_card(self, **kwargs):
        return self._do_action(**kwargs)

    def get_bindings(self, **kwargs):
        return self._do_action(**kwargs)

    def get_extended_order_status(self, **kwargs):
        return self._do_action(**kwargs)

    def get_last_orders_for_merchants(self, **kwargs):
        return self._do_action(**kwargs)

    def reverse_order(self, **kwargs):
        return self._do_action(**kwargs)

    def register_order(self, **kwargs):
        return self._do_action(**kwargs)
