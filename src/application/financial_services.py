from src.application.categorization_service import Categorizer
from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
import pandas as pd
from dateutil.relativedelta import relativedelta
import streamlit as st


class DashboardService:

    def __init__(self):
        self.repo = SQLiteTransactionRepository(db=DataBaseSession())
        self.service = TransactionService(self.repo)

    @st.cache_data
    def get_monthly_comparison(_self, current_month, current_year):
        """
        :param current_month: wanted month as string
        :param current_year: current year as string
        :return: wanted month's spending, spending difference as percentage
        """
        current_date = pd.to_datetime(f"{current_year}-{current_month}", format='%Y-%B')
        last_date = current_date - pd.DateOffset(months=1)

        current_period = current_date.to_period('M')
        last_period = last_date.to_period('M')

        df = _self.service.get_expenses()
        df.set_index('date', inplace=True)
        df1 = df.groupby(df.index.to_period('M'))['amount'].sum()

        current_amount = abs(df1.get(current_period, 0))
        last_amount = abs(df1.get(last_period, 0))

        if current_amount == 0:
            dif = 0.0
        else:
            dif = (current_amount - last_amount) * 100 / last_amount
            dif = round(dif,1)

        current_amount = round(current_amount,0)

        return current_amount, dif

    @st.cache_data
    def get_burn_rate_data(_self, month, year):

        df = _self.service.get_expenses()
        current_date = pd.to_datetime(f"{year}-{month}", format='%Y-%B')
        last_date = current_date - pd.DateOffset(months=1)

        current_month = current_date.strftime('%B %Y')
        last_month = last_date.strftime('%B %Y')

        df1 = df.groupby('date')['amount'].sum().abs().reset_index()
        df1['day'] = df1['date'].dt.day
        df1['month'] = df1['date'].dt.strftime('%B %Y')
        df1['cumulative_amount'] = df1.groupby('month')['amount'].cumsum()

        df2 = df1[df1['month'].isin([current_month,last_month])]
        return df2

    @st.cache_data
    def get_top_expenses(_self, month, year):
        df = _self.service.get_expenses()
        date = pd.to_datetime(f"{year}-{month}", format='%Y-%B')
        month = date.strftime('%B %Y')

        df['month'] = df['date'].dt.strftime('%B %Y')
        df1 = df[df['month'] == month]
        df1['amount'] = df1['amount'].abs()
        df2 = df1.nlargest(5,'amount')

        df3 = df2.loc[:,['amount', 'description', 'category']]

        return df3

    @st.cache_data
    def get_predicted_expenses(_self, month, year):
        df = _self.service.get_expenses()
        date = pd.to_datetime(f"{year}-{month}", format='%Y-%B')
        month = date.strftime('%B %Y')

        df['month'] = df['date'].dt.strftime('%B %Y')
        df1 = df[df['month'] == month]
        df1['amount'] = df1['amount'].abs()

        df2 = df1[df1['category'].str.endswith('(Predicted)')]
        df3 = df2.loc[:, ['amount', 'description', 'category', 'id']]
        df3.sort_values(by = 'amount', ascending = False, inplace = True)
        return df3

class FinancialService:
        def __init__(self):
            self.repo = SQLiteTransactionRepository(db=DataBaseSession())
            self.service = TransactionService(self.repo)

        @st.cache_data
        def get_expenses_by_month(_self, month, year):
            df = _self.service.get_expenses()
            current_month = f"{month} {year}"
            df['month'] = df['date'].dt.strftime('%B %Y')

            return df[df['month'] == current_month]

        @st.cache_data
        def get_expenses_by_month_interval(_self, first_month, first_year, second_month, second_year):
            df = _self.service.get_expenses()
            df['month'] = df['date'].dt.strftime('%B %Y')

            first_date = pd.to_datetime(f"{first_month} {first_year}", format = '%B %Y')
            second_date = pd.to_datetime(f"{second_month} {second_year}", format = '%B %Y')
            if first_date > second_date:
                temp = first_date
                first_date = second_date
                second_date = temp

            current_date = first_date

            months_list = []
            while current_date <= second_date:
                months_list.append(current_date.strftime('%B %Y'))
                current_date = current_date + relativedelta(months = 1)

            df1 = df[df['month'].isin(months_list)]
            return df1

        def get_expenses(_self):
            return _self.service.get_expenses()

        @st.cache_data
        def get_category_list(_self):
            transaction_list = _self.repo.get_all_transactions()
            category_service = Categorizer(transaction_list)
            return list(category_service.dict.keys())

        def get_transactions_by_category(_self, _df, category):
            """
            :param _df: Dataframe to be filtered with a specific category
            :param category: Wanted category
            :return:
            """
            if category == 'ALL':
                return _df
            else:
                df1 = _df[_df['category'] == category]
                return df1

        def get_all_transactions(_self):
            return _self.service.get_all_transactions()

        @st.cache_data
        def get_all_transactions_by_month(_self, month, year):
            df = _self.service.get_all_transactions()
            current_month = f"{month} {year}"
            df['month'] = df['date'].dt.strftime('%B %Y')

            return df[df['month'] == current_month]

        def update_transaction_category(self, edited_df):
            for index, row in edited_df.iterrows():
                _id = row['id']
                new_category = row['category']
                self.repo.update_transaction_category(_id, new_category)

