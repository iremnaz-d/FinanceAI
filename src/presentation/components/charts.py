import plotly.express as px
from src.application.financial_services import DashboardService
from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository

class FinancialVisualizer:
    """
    This class returns all the charts needed for the interface using Plotly Express
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
        """
        :return: Pie chart of expenses without predictions (amount/category)
        """
        df = self.service.get_expenses()
        df['category'] = df['category'].replace(r'.*\(Predicted\)$', 'Other', regex=True)
        df1 = df.groupby('category')['amount'].sum().abs().reset_index()
        figure = px.pie(df1,values = 'amount', names = 'category')
        return figure

    def pie_category_expense_with_predictions(self):
        """
        :return: Pie chart of expenses with predictions (amount/category)
        """
        df = self.service.get_expenses()
        df['category'] = df['category'].str.replace(' (Predicted)', '', regex = False)
        df = df[df['category'] != 'Income']
        df1 = df.groupby('category')['amount'].sum().abs().reset_index()
        figure = px.pie(df1, values = 'amount', names = 'category')
        return figure

    def line_burn_rate(self, month, year):
        """
        :param month: wanted month
        :param year: wanted year
        :return: Burn Rate chart comparing two months for the dashboard
        """
        dService = DashboardService()
        df= dService.get_burn_rate_data(month,year)
        figure = px.line(df, x = 'day', y = 'cumulative_amount', color = 'month')
        figure.update_layout(xaxis_title = 'Days', yaxis_title = 'Expense (Cumulative)')
        return figure