from payment_app.payment_app.core.factory import PaymentServiceFactory
from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface
from payment_app.payment_app.domain.payment import PaymentType


class MembershipUpgradePaymentPlugin(PaymentPluginInterface):
    def process_payment(self):
        # ToDo Implementation business rules about upgrade membership
        return "Upgraded membership"


def register() -> None:
    PaymentServiceFactory.register(PaymentType.MEMBERSHIP_UPGRADE.value,
                                   MembershipUpgradePaymentPlugin)
