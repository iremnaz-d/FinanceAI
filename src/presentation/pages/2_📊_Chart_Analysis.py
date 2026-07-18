import sys
import os
from dataclasses import asdict

from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
from src.presentation.components.charts import FinancialVisualizer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chart Analysis", page_icon="📊", layout="wide")

def choice_chart():
   chart_type =  st.selectbox('Select a chart: ', ['Line Chart'])
   data_type = st.radio("I want to see: ", ['All Transactions', 'Only Expenses', 'Only Revenues'])
   return chart_type, data_type

def main():

    repo = SQLiteTransactionRepository(db=DataBaseSession())
    transaction_list = repo.get_all_transactions()
    df = pd.DataFrame([asdict(data) for data in transaction_list])
    vis = FinancialVisualizer(df = df) #visualizer on charts.py

    chart_type, data_type = choice_chart()

    if chart_type == 'Line Chart':
        if data_type == 'All Transactions':
            fig = vis.plot_daily_trend()
            st.plotly_chart(fig)

if __name__ == '__main__':
    main()



