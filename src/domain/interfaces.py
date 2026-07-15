from abc import ABC, abstractmethod


class TransactionRepository(ABC):
    """
    TransactionRepository(ABC): Veritabanı işlemlerinin (kaydetme, listeleme) altyapıdan
    bağımsız şekilde tanımlandığı soyut sınıf (Interface).
    """

class PredictiveModel(ABC):
    """
    PredictiveModel(ABC): ML modellerinin uyması gereken
    train ve predict metotlarını dikte eden soyut altyapı.
    """