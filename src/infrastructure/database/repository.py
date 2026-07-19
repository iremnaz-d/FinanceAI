from datetime import datetime
from src.domain.entities import Transaction
from src.domain.interfaces import TransactionRepository
from src.infrastructure.database.db_connection import DataBaseSession
from sqlalchemy import select
from src.infrastructure.database.db_models import SQLAlchemyTransaction

class SQLiteTransactionRepository(TransactionRepository):

    """
    This class queries databases applying the abstract TransactionRepository interface in the interfaces.py module
    """

    def __init__(self, db: DataBaseSession):
        self.db = db

    def add_transaction(self, transaction: Transaction):

        session = self.db.get_session()
        try:
            db_transaction = SQLAlchemyTransaction(
                _id= transaction.id,
                date=transaction.date,
                description=transaction.description,
                amount=transaction.amount,
                balance=transaction.balance,
                category = transaction.category
            )
            session.add(db_transaction)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()



    def get_all_transactions(self):
        """
        :return: Transaction list from repository
        """
        session = self.db.get_session()
        try:
            statement = select(SQLAlchemyTransaction)
            _list = session.scalars(statement).all()
            return Transaction.from_db_model_plural(_list)

        finally:
            session.close()

    def get_transaction_by_id(self, _id: str):
        """
        :param _id: Transaction ID (str) (Primary Key)
        :return: Transaction
        """
        session = self.db.get_session()
        try:
            transaction = session.get(SQLAlchemyTransaction, _id)
            if transaction is None:
                return None
            return Transaction.from_db_model(transaction)

        finally:
            session.close()

    def get_transactions_by_date(self, date: datetime):
        """
        :param date: Transaction date (datetime)
        :return: Transaction list
        """
        session = self.db.get_session()
        try:
            statement = select(SQLAlchemyTransaction).where(SQLAlchemyTransaction.date == date)
            _list = session.scalars(statement).all()
            return Transaction.from_db_model_plural(_list)

        finally:
            session.close()
            
    def check_if_exists(self, _id: str):
        return self.get_transaction_by_id(_id) is not None
