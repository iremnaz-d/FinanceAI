from abc import ABC, abstractmethod
from datetime import datetime
from src.domain.entities import Transaction


class TransactionRepository(ABC):
    """
    An abstract class (interface) in which database operations (insertion, retrieval) are
    defined independently of the underlying infrastructure.
    """

    @abstractmethod
    def get_all_transactions(self):
        pass

    @abstractmethod
    def add_transaction(self, transaction: Transaction):
        pass

    @abstractmethod
    def delete_transaction(self, _id):
        pass


    @abstractmethod
    def get_transaction_by_id(self, _id: str):
        pass

