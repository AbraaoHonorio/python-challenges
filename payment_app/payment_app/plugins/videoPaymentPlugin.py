from payment_app.payment_app.core.factory import PaymentServiceFactory
from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface
from payment_app.payment_app.domain.payment import PaymentType


class VideoPaymentPlugin(PaymentPluginInterface):
    def process_payment(self):
        # ToDo Implementation business rules about free record video
        return "Added free video to shipping label"


def register() -> None:
    PaymentServiceFactory.register(PaymentType.VIDEO.value,
                                   VideoPaymentPlugin)
