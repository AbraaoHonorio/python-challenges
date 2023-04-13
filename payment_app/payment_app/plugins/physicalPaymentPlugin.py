from payment_app.payment_app.core.factory import PaymentServiceFactory
from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface
from payment_app.payment_app.domain.payment import PaymentType


class PhysicalPaymentPlugin(PaymentPluginInterface):
    def process_payment(self):
        # ToDo Implementation business rules about shipping label
        return "Generated shipping label for physical product"


def register() -> None:
    PaymentServiceFactory.register(PaymentType.PHYSICAL.value,
                                   PhysicalPaymentPlugin)
