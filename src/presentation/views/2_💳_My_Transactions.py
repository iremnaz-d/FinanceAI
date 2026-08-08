import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

from src.application.financial_services import FinancialService
import streamlit as st
import datetime

st.set_page_config(page_title="My Transaction History", page_icon="💳", layout="wide")

def main():
    st.title("My Transactions 💳")
    financial_service = FinancialService()

    today = datetime.date.today()
    months = ['ALL']
    for i in range(24):
        date = today - datetime.timedelta(days=i * 30)
        formatted_date = date.strftime('%B %Y')
        if formatted_date not in months:
            months.append(formatted_date)

    col1, col2 = st.columns(2)

    with col1:
        period = st.selectbox('Choose month: ', months)
        if period == 'ALL':
            df = financial_service.get_all_transactions()
        else:
            current_month, current_year = period.split()
            df = financial_service.get_all_transactions_by_month(current_month, current_year)

    with col2:
        category_list = financial_service.get_category_list()
        category_list.insert(0, 'ALL')
        category = st.selectbox('Choose category:', category_list)
        df1 = financial_service.get_transactions_by_category(df,category)

    event = st.dataframe(df1,
                         on_select = "rerun",
                         selection_mode = "single-row",
                         height = 700)


    selected_rows = event.selection.rows

    if len(selected_rows)>0:
        index = selected_rows[0]
        _id = df1.iloc[index]['id']

        col3,col4 = st.columns([5,1])
        with col4:
            if st.button("🗑️ Delete Selected Transaction", type = "primary"):
                financial_service.delete_transaction(_id)
                st.cache_data.clear()
                st.success("Transaction Removed!")
                st.rerun()



main()