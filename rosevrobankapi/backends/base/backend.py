from six import with_metaclass

from rosevrobankapi.exceptions import ImproperlyConfigured


class BackendMetaclass(type):
    @staticmethod
    def __new__(mcs, name, bases, attrs):
        if not attrs.get('name') and name != 'BaseBackend':
            raise ImproperlyConfigured("Backend's 'name' attribute is not configured for %s backend" % name)
        return super(BackendMetaclass, mcs).__new__(mcs, name, bases, attrs)


class BaseBackend(with_metaclass(BackendMetaclass)):
    name = None

    PARAM_ERROR_CODE = 'errorCode'
    PARAM_ERROR_MESSAGE = 'errorMessage'

    parameter_map = (
        ('acs_url', 'acsUrl'),
        ('action_code', 'actionCode'),
        ('action_code_description', 'actionCodeDescription'),
        ('approval_code', 'approvalCode'),
        ('approved_amount', 'approvedAmount'),
        ('auth_code', 'authCode'),
        ('auth_date_time', 'authDateTime'),
        ('auth_reference_number', 'authRefNum'),
        ('bank_country_code', 'bankCountryCode'),
        ('bank_country_name', 'bankCountryName'),
        ('bank_info', 'bankInfo'),
        ('bank_name', 'bankName'),
        ('binding_id', 'bindingId'),
        ('binding_info', 'bindingInfo'),
        ('card_auth_info', 'cardAuthInfo'),
        ('cardholder_name', 'cardholderName'),
        ('client_id', 'clientId'),
        ('deposit_amount', 'depositAmount'),
        ('deposited_amount', 'depositedAmount'),
        ('emitter_name', 'emitterName'),
        ('emitter_country_code', 'emitterCountryCode'),
        ('error_code', 'ErrorCode'),
        ('error_code', 'errorCode'),
        ('error_message', 'errorMessage'),
        ('error_message', 'ErrorMessage'),
        ('expiration_date', 'expirationDate'),
        ('expiry_date', 'expiryDate'),
        ('fail_url', 'failUrl'),
        ('form_url', 'formUrl'),
        ('is_enrolled', 'isEnrolled'),
        ('json_params', 'jsonParams'),
        ('masked_pan', 'maskedPan'),
        ('md_order', 'mdOrder'),
        ('merchant_order_params', 'merchantOrderParams'),
        ('new_expiry', 'newExpiry'),
        ('order_id', 'orderId'),
        ('order_number', 'OrderNumber'),
        ('order_number', 'orderNumber'),
        ('order_description', 'orderDescription'),
        ('order_status', 'OrderStatus'),
        ('order_status', 'orderStatus'),
        ('order_statuses', 'orderStatuses'),
        ('page_view', 'pageView'),
        ('page_size', 'pageSize'),
        ('payment_authentication_request', 'paReq'),
        ('payment_amount_info', 'paymentAmountInfo'),
        ('payment_state', 'paymentState'),
        ('refunded_amount', 'refundedAmount'),
        ('return_url', 'returnUrl'),
        ('session_timeout', 'sessionTimeoutSec'),
        ('term_url', 'termUrl'),
        ('terminal_id', 'terminalId'),
        ('total_count', 'totalCount'),
        ('transaction_states', 'transactionStates'),
        ('user_name', 'userName'),
    )

    parameter_map_reverse = set([(p1, p0) for p0, p1 in parameter_map])

    def __init__(self, **kwargs):
        self.raise_errors = kwargs.pop('raise_errors', False)

    def register_order(self, **kwargs):
        raise NotImplementedError()

    def reverse_order(self, **kwargs):
        raise NotImplementedError()

    def refund(self, **kwargs):
        raise NotImplementedError()

    def get_order_status(self, **kwargs):
        raise NotImplementedError()

    def get_extended_order_status(self, **kwargs):
        raise NotImplementedError()

    def verify_enrolling(self, **kwargs):
        raise NotImplementedError()

    def get_last_orders_for_merchants(self, **kwargs):
        raise NotImplementedError()

    def pre_auth_register_order(self, **kwargs):
        raise NotImplementedError()

    def deposit(self, **kwargs):
        raise NotImplementedError()

    def payment_order_binding(self, **kwargs):
        raise NotImplementedError()

    def unbind_card(self, **kwargs):
        raise NotImplementedError()

    def extend_binding(self, **kwargs):
        raise NotImplementedError()

    def get_bindings(self, **kwargs):
        raise NotImplementedError()


class AuthBackendMixin(object):
    PARAM_USER_NAME = 'userName'
    PARAM_PASSWORD = 'password'

    user_name = None
    password = None

    def set_secure(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def _append_secure(self, params):
        params[self.PARAM_USER_NAME] = self.user_name
        params[self.PARAM_PASSWORD] = self.password
