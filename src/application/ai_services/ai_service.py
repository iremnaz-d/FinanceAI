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

        with open("src/application/ai_services/prompts/system_prompt.txt", "r", encoding = "utf-8") as f:
            raw_system_prompt = f.read()

        system_prompt = raw_system_prompt.format(
            dataframe = markdown_df,
            user_query = user_question
        )

        response = self.client.generate_response(system_prompt)
        return response, timeframe

    def _get_timeframe(self, user_query, init_timeframe): #router for timeframe
        current_date = datetime.now().strftime('%B %Y')

        with open("src/application/ai_services/prompts/router_prompt.txt", "r", encoding = "utf-8") as f:
            raw_router_prompt = f.read()

        router_prompt = raw_router_prompt.format(
            current_date = current_date,
            init_timeframe = init_timeframe,
            user_query = user_query
        )

        response = self.client.generate_response(router_prompt)
        return response
