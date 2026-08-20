import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from src.presentation.components.dashboard import DashboardFeatures
import streamlit as st
from src.infrastructure.database.migration import DataBaseMigrator

st.set_page_config(page_title="Homepage", page_icon="🏠", layout="wide")

def init_database():
    """
    Database Initialization.
    If the file has been uploaded and the system is ready, the migration is performed.
    Otherwise, the user is directed to upload the file.
    """
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

def main():

    image_path = "src/presentation/components/images/logo_text.png"
    st.image(image_path, width=400)
    st.write("")

    init_database()

    dashboard = DashboardFeatures() #src/presentation/components/dashboard.py
    dashboard.monthly_view()

main()