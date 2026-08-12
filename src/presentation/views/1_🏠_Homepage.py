import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from src.presentation.components.dashboard import DashboardFeatures
from dataclasses import asdict
import streamlit as st
import pandas as pd
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.migration import DataBaseMigrator
from src.infrastructure.database.repository import SQLiteTransactionRepository

st.set_page_config(page_title="Homepage", page_icon="🏠", layout="wide")


def init_database():
    migrator = DataBaseMigrator()
    try:
        migrator.run_migration()
        st.session_state.is_file_uploaded = True
        if not st.session_state.system_ready:
            st.session_state.system_ready = True
            st.rerun()
    except Exception:
        st.session_state.is_file_uploaded = False
        st.error("Please upload your transaction file from '📁 Data Management'.")
        st.stop()

    repo = SQLiteTransactionRepository(db=DataBaseSession())

    transaction_list = repo.get_all_transactions()
    df = pd.DataFrame([asdict(data) for data in transaction_list])

def main():

    image_path = "src/presentation/components/logo_text.png"
    st.image(image_path, width=400)
    st.write("")

    init_database()

    dashboard = DashboardFeatures()
    dashboard.monthly_view()

main()