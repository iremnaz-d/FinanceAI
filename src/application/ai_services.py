from src.application.financial_services import FinancialService
from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
from src.infrastructure.llm.client import Client
from datetime import datetime


class AIService:

    def __init__(self):
        self.client = Client()
        self.financial_service = FinancialService()
        self.repo = SQLiteTransactionRepository(db=DataBaseSession())
        self.transaction_service = TransactionService(self.repo)

    def get_financial_insight(self, user_question, init_timeframe):
        timeframe = self._get_timeframe(user_question, init_timeframe)
        if timeframe == 'ALL':
            df = self.transaction_service.get_expenses()
        else:
            try:
                args = timeframe.split()
                if len(args) == 2:
                    month, year = timeframe.split(" ")
                    df = self.financial_service.get_expenses_by_month(month, year)
                else:
                    first_month, first_year, second_month, second_year = timeframe.split(" ")
                    df = self.financial_service.get_expenses_by_month_interval(first_month, first_year, second_month, second_year)

            except ValueError:
                df = self.transaction_service.get_expenses()

        markdown_df = df.to_markdown(index = False)

        system_prompt = ("You are an expert Finance Assistant who has a nice humor. "
                         "While you analyze the financial tables you are given, you will follow these rules:"
                         "1. You stay loyal to the given information in the supplied table, no outside made-up information."
                         )
        table_info = f"User's expense data in this month is {markdown_df}."
        whole_prompt = f"{system_prompt} {table_info} According to these information, answer the user's question: {user_question}"

        response = self.client.generate_response(whole_prompt)
        return response, timeframe

    def _get_timeframe(self, user_query, init_timeframe):
        current_date = datetime.now().strftime('%B %Y')

        router_prompt = f"""
        You are a router that extracts the requested timeframe from a user's financial question.
        The current date is {current_date}.
        
        Rules:
        1. If the user asks about a specific month, output it in 'Month YYYY' format (e.g., 'March 2026').
        2. If the user asks about 'this month', output '{current_date}'.
        3. If the user asks about all their data, output 'ALL'.
        4. If the user doesn't specify a time, output {init_timeframe}.
        5. If the user wants a time interval, output the interval in 'Month YYYY Month YYYY' format (e.g., 'January 2026 March 2026').
        6. Output ONLY the timeframe or 'ALL'. Do not write any other words or punctuation.
        
        User Question: {user_query}
        """

        response = self.client.generate_response(router_prompt)
        return response
