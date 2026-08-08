from src.application.categorization_service import Categorizer
from src.application.ml_services import TransactionPredictor
from src.config.settings import Settings
from src.infrastructure.data.excel_parser import ExcelReader
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
import random
import string

class DataBaseMigrator:

    def __init__(self):
        self.db = DataBaseSession()
        self.repo = SQLiteTransactionRepository(self.db)
        self.excell_reader = ExcelReader(Settings.FILE_PATH)

    def run_migration(self):
        transaction_list = self.excell_reader.read()

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


            else:
                if other_transaction.amount != transaction.amount:
                    random_id = self.generate_random_id()
                    transaction.set_id(random_id)
                    self.repo.add_transaction(transaction)
                    count += 1



            # if not self.repo.check_if_exists(transaction.id):
            #     self.repo.add_transaction(transaction)
            #     count += 1

        print(f"Migration is complete. {count} new transaction is added to the database.")

    def generate_random_id(self):
        """
        There are some transactions which have the same IDs.
        This method is used for generating a new ID for these kind of transactions.
        :return: string id
        """
        length = 8
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k = length))




