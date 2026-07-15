from abc import ABC, abstractmethod
from datetime import datetime


class TransactionRepository(ABC):
    """
    TransactionRepository(ABC): Veritabanı işlemlerinin (kaydetme, listeleme) altyapıdan
    bağımsız şekilde tanımlandığı soyut sınıf (Interface).
    """

    @abstractmethod
    def get_all_transactions(self):
        pass

    def get_transactions_by_date(self, date: datetime):
        pass

    def get_transaction_by_id(self, id: str):
        pass

class PredictiveModel(ABC):
    """
    PredictiveModel(ABC): ML modellerinin uyması gereken
    train ve predict metotlarını dikte eden soyut altyapı.
    """