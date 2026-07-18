import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from dataclasses import asdict
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.migration import DataBaseMigrator
from src.infrastructure.database.repository import SQLiteTransactionRepository
import pandas as pd
import streamlit as st

st.set_page_config(page_title="My Transaction History", page_icon="💳", layout="wide")

def main():

    repo = SQLiteTransactionRepository(db=DataBaseSession())
    transaction_list = repo.get_all_transactions()
    df = pd.DataFrame([asdict(data) for data in transaction_list])

    st.dataframe(df, height = 700)

if __name__ == '__main__':
    main()