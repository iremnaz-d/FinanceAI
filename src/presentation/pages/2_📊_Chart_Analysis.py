import sys
import os
from dataclasses import asdict

from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
from src.presentation.components.charts import FinancialVisualizer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chart Analysis", page_icon="📊", layout="wide")

def choice_chart():
   chart_type =  st.selectbox('Select a chart: ', ['Line Chart', 'Pie Chart'])
   return chart_type

def choice_data():
    data_type = st.radio("I want to see: ", ['All Transactions', 'Only Expenses', 'Only Incomes'])
    return data_type


def main():

    vis = FinancialVisualizer() # Plotly visualizer on charts.py

    chart_type= choice_chart()

    if chart_type == 'Line Chart':
        data_type = choice_data()
        fig = None
        match data_type:
            case 'All Transactions':
                fig = vis.line_daily_trend()
            case 'Only Expenses':
                fig = vis.line_daily_trend_expense()
            case 'Only Incomes':
                fig = vis.line_daily_trend_income()
        st.plotly_chart(fig)

    elif chart_type == 'Pie Chart':
        st.markdown("## My Spendings")
        fig = vis.pie_category_expense()
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()



