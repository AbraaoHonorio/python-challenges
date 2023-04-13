from abc import ABC, abstractmethod


class PaymentPluginInterface(ABC):
    @abstractmethod
    def process_payment(self):
        pass
