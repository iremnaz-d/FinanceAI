from dataclasses import asdict

import plotly.express as px
import pandas as pd

from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository





class FinancialVisualizer:
    """
    FinancialVisualizer: Plotly veya Matplotlib kullanarak pasta grafikleri,
    harcama trend çizgileri ve kategori dağılımlarını çizen arayüz sınıfı.
    """
    def __init__(self):
        self.repo = SQLiteTransactionRepository(db=DataBaseSession())
        self.service = TransactionService(self.repo)

    def line_daily_trend(self):
        """
        :return: Line Chart of all the transactions in account (date/profit)
        """
        df = self.service.get_all_transactions()
        df1 = df.groupby('date')['amount'].sum().reset_index()
        figure = px.line(df1, x='date', y='amount')
        return figure

    def line_daily_trend_expense(self):
        """
        :return: Line Chart of expenses (date/amount)
        """
        df = self.service.get_expenses()
        df1 = df.groupby('date')['amount'].sum().reset_index()
        figure = px.line(df1, x = 'date', y = 'amount')
        figure.update_yaxes(autorange="reversed") #to show negative values above x-axes
        return figure

    def line_daily_trend_income(self):
        """
        :return: Line Chart of incomes (date/amount)
        """
        df = self.service.get_incomes()
        df1 = df.groupby('date')['amount'].sum().reset_index()
        figure = px.line(df1, x = 'date', y = 'amount')
        return figure

    def pie_category_expense(self):
        df = self.service.get_expenses()
        df1 = df.groupby('category')['amount'].sum().abs().reset_index()
        figure = px.pie(df1,values = 'amount', names = 'category')
        return figure





"""if __name__ == '__main__':
     repo = SQLiteTransactionRepository(db=DataBaseSession())
     transaction_list = repo.get_all_transactions()
     df = pd.DataFrame([asdict(data) for data in transaction_list])

     vis = FinancialVisualizer(df)

     vis.plot_daily_trend(df) """



