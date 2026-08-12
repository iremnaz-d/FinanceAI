import sys
import os

from src.infrastructure.database.migration import DataBaseMigrator

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

import streamlit as st
import time

st.title("Data Management 📁")

with st.container(border = True):
    st.write("You can upload your bank account transactions in here. (Must be an :green[.xlsx] file)")

    uploaded_file = st.file_uploader("Transaction History (Excel)", type=["xlsx"])

    if uploaded_file is not None:
        st.write("Please wait for the upload...")
        save_path = "src/data/Transaction_History.xlsx"
        save_dir = os.path.dirname(save_path)

        try:
            os.makedirs(save_dir, exist_ok = True)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            migrator = DataBaseMigrator()
            migrator.run_migration()
            st.cache_data.clear()

            st.success("✅ File successfully uploaded and system data is updated.")
            st.success("↩️ Redirecting you to Homepage...")
            st.session_state.system_ready = True
            time.sleep(3)
            st.switch_page("views/1_🏠_Homepage.py")

        except Exception as e:
            st.error(f"An error occurred during file upload: {e}")


