from enum import Enum


class PaymentType(Enum):
    BOOK = "book"
    MEMBERSHIP = "membership"
    MEMBERSHIP_UPGRADE = "membership_upgrade"
    PHYSICAL = "physical"
    VIDEO = "video"


class Payment:
    def __init__(self, payment_type: PaymentType):
        self.payment_type = payment_type
