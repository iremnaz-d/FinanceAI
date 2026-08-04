import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

from src.application.financial_services import DashboardService
from src.presentation.components.dashboard import DashboardFeatures
from dataclasses import asdict
import streamlit as st
import pandas as pd
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.migration import DataBaseMigrator
from src.infrastructure.database.repository import SQLiteTransactionRepository

st.set_page_config(page_title="Homepage", page_icon="🏠", layout="wide")
homepage = st.Page("app.py", title="Homepage", icon="🏠")
pg = st.navigation([homepage])
pg.run()


def init_database():
    migrator = DataBaseMigrator()
    migrator.run_migration()

    repo = SQLiteTransactionRepository(db=DataBaseSession())
    transaction_list = repo.get_all_transactions()
    df = pd.DataFrame([asdict(data) for data in transaction_list])



def main():
    st.title("FinanceAI")

    init_database()

    dashboard = DashboardFeatures()
    dashboard.monthly_view()



if __name__ == "__main__":
    main()