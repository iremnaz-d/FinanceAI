import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from src.presentation.components.charts import FinancialVisualizer
import streamlit as st

st.set_page_config(page_title="Chart Analysis", page_icon="📊", layout="wide")

def choice_chart():
   chart_type =  st.selectbox('See my: ', ['Transaction flow over year', 'Expenses over categories'])
   return chart_type

def choice_data():
    data_type = st.radio("I want to see: ", ['All Transactions', 'Only Expenses', 'Only Incomes'])
    return data_type

def main():
    st.title("Chart Analysis 📊")

    if not st.session_state.is_file_uploaded:
        st.error("Please upload your transaction file from '📁 Data Management'.")
        st.stop()

    vis = FinancialVisualizer() # Plotly visualizer on charts.py

    chart_type= choice_chart()

    if chart_type == 'Transaction flow over year':
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

    elif chart_type == 'Expenses over categories':
        st.markdown("## My Spendings")
        if st.checkbox('Predict uncategorized payments'):
            fig = vis.pie_category_expense_with_predictions()
        else:
            fig = vis.pie_category_expense()
        st.plotly_chart(fig)


main()



