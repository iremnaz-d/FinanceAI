from src.application.categorization_service import Categorizer
from src.application.ml_services import TransactionPredictor
from src.config.settings import Settings
from src.infrastructure.data.excel_parser import ExcelReader
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository

class DataBaseMigrator:
    """
    This class is where all tasks —including reading files, cleaning data, categorizing,
     making ML predictions, and adding the final data to the database— come together.
    """

    def __init__(self):
        self.db = DataBaseSession()
        self.repo = SQLiteTransactionRepository(self.db)
        self.excell_reader = ExcelReader(Settings.FILE_PATH)

    def run_migration(self):
        try:
            transaction_list = self.excell_reader.read()
        except Exception as e:
            return e

        categorizer = Categorizer(transaction_list)
        new_transaction_list = categorizer.categorize()

        predictor = TransactionPredictor(new_transaction_list)
        brand_new_transaction_list = predictor.predict_category()
        count = 0

        for transaction in brand_new_transaction_list:
            other_transaction = self.repo.get_transaction_by_id(transaction.id)
            if other_transaction is None:
               self.repo.add_transaction(transaction)
               count += 1

        print(f"Migration is complete. {count} new transaction is added to the database.")
        return None