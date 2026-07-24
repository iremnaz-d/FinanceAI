from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
import pandas as pd


class DashboardService:

    def __init__(self):
        self.repo = SQLiteTransactionRepository(db=DataBaseSession())
        self.service = TransactionService(self.repo)

    def get_monthly_comparison(self, current_month, current_year):
        """
        :param current_month: wanted month as string
        :param current_year: current year as string
        :return: wanted month's spending, spending difference as percentage
        """
        current_date = pd.to_datetime(f"{current_year}-{current_month}", format='%Y-%B')
        last_date = current_date - pd.DateOffset(months=1)

        current_period = current_date.to_period('M')
        last_period = last_date.to_period('M')

        df = self.service.get_expenses()
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

    def get_burn_rate_data(self, month, year):

        df = self.service.get_expenses()
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





