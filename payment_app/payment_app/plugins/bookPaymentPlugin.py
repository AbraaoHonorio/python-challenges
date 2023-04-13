from payment_app.payment_app.core.factory import PaymentServiceFactory
from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface
from payment_app.payment_app.domain.payment import PaymentType


class BookPaymentPlugin(PaymentPluginInterface):
    def process_payment(self):
        # ToDo Implementation business rules about duplicate shipping label
        return "Generated duplicate shipping label for book"


def register() -> None:
    PaymentServiceFactory.register(PaymentType.BOOK.value, BookPaymentPlugin)
