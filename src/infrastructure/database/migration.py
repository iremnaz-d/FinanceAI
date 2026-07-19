from src.application.categorization_service import Categorizer
from src.config.settings import Settings
from src.infrastructure.data.excel_parser import ExcellReader
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository

class DataBaseMigrator:

    def __init__(self):
        self.db = DataBaseSession()
        self.repo = SQLiteTransactionRepository(self.db)
        self.excell_reader = ExcellReader(Settings.FILE_PATH)

    def run_migration(self):
        transaction_list = self.excell_reader.read()
        categorizer = Categorizer(transaction_list)
        new_transaction_list = categorizer.categorize()
        count = 0

        for transaction in new_transaction_list:
            if not self.repo.check_if_exists(transaction.id):
                self.repo.add_transaction(transaction)
                count += 1

        print(f"Migration is complete. {count} new transaction is added to the database.")



