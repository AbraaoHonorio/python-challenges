from payment_app.payment_app.core.factory import PaymentServiceFactory
from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface
from payment_app.payment_app.domain.payment import PaymentType


class MembershipPaymentPlugin(PaymentPluginInterface):

    def process_payment(self):
        # ToDo Implementation business rules about activate membership
        return "Activated membership"


def register() -> None:
    PaymentServiceFactory.register(PaymentType.MEMBERSHIP.value,
                                   MembershipPaymentPlugin)
