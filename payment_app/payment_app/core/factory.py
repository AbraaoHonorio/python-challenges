"""Factory for creating a payment by your type."""
from typing import Optional

from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface
from payment_app.payment_app.domain.paymentException import PaymentException


class PaymentServiceFactory:
    _payment_creation_funcs = {}

    @staticmethod
    def get_by_type(payment_type) -> Optional[PaymentPluginInterface]:
        """Return a payment by your type."""
        return PaymentServiceFactory._payment_creation_funcs.get(payment_type)

    @staticmethod
    def register(payment_type, creator_fn):
        """Register a new payment type."""
        PaymentServiceFactory._payment_creation_funcs[payment_type] = creator_fn

    @staticmethod
    def unregister(payment_type):
        """Unregister a payment type."""
        PaymentServiceFactory._payment_creation_funcs.pop(payment_type, None)

    @staticmethod
    def create(arguments) -> PaymentPluginInterface:
        """Create a payment of a specific type, given JSON data."""
        args_copy = arguments.copy()
        payment_type = args_copy.pop("type")
        try:
            payment_plugin = PaymentServiceFactory.get_by_type(payment_type)
            return payment_plugin()
        except Exception as e:
            raise PaymentException(f"unknown payment type {payment_type!r}. Error: {e}")