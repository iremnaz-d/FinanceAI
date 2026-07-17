from dataclasses import asdict
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.migration import DataBaseMigrator
from src.infrastructure.database.repository import SQLiteTransactionRepository
from src.presentation.components.charts import FinancialVisualizer
import pandas as pd

if __name__ == '__main__':

    migrator = DataBaseMigrator()
    migrator.run_migration()

    repo = SQLiteTransactionRepository(db=DataBaseSession())
    transaction_list = repo.get_all_transactions()
    df = pd.DataFrame([asdict(data) for data in transaction_list])

    vis = FinancialVisualizer(df)

    vis.plot_daily_trend()

