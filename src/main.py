from dataclasses import asdict
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.migration import DataBaseMigrator
from src.infrastructure.database.repository import SQLiteTransactionRepository
import pandas as pd

if __name__ == '__main__':
    """
    I created this module to understand the cause of certain errors.
    It isn't currently being used in the project, but I won't delete it anyway—it might come in handy.
    """

    migrator = DataBaseMigrator()
    migrator.run_migration()

    repo = SQLiteTransactionRepository(db=DataBaseSession())
    transaction_list = repo.get_all_transactions()
    df = pd.DataFrame([asdict(data) for data in transaction_list])

    with pd.option_context('display.max_columns', None):
        print(df.head(15))