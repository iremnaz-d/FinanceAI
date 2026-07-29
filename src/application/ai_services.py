from src.application.financial_services import FinancialService
from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
from src.infrastructure.llm.client import Client


class AIService:

    def __init__(self):
        self.client = Client()
        self.financial_service = FinancialService()
        self.repo = SQLiteTransactionRepository(db=DataBaseSession())
        self.transaction_service = TransactionService(self.repo)

    def get_financial_insight(self, user_question, month, year):
        df = self.financial_service.get_expenses_by_month(month,year)
        markdown_df = df.to_markdown(index = False)

        system_prompt = ("You are an expert Finance Assistant who has a nice humor. "
                         "While you analyze the financial tables you are given, you will follow these rules:"
                         "1. You stay loyal to the given information in the supplied table, no outside made-up information."
                         )
        table_info = f"User's expense data in this month is {markdown_df}."
        whole_prompt = f"{system_prompt} {table_info} According to these information, answer the user's question: {user_question}"

        response = self.client.generate_response(whole_prompt)
        return response





