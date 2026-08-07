from src.application.financial_services import FinancialService
from src.application.transaction_service import TransactionService
from src.infrastructure.database.db_connection import DataBaseSession
from src.infrastructure.database.repository import SQLiteTransactionRepository
from src.infrastructure.llm.client import Client
from datetime import datetime
import json
from google.genai import types


class AIService:

    def __init__(self):
        self.client = Client()
        self.financial_service = FinancialService()
        self.repo = SQLiteTransactionRepository(db=DataBaseSession())
        self.transaction_service = TransactionService(self.repo)

    def get_financial_insight(self, user_question, init_timeframe):
        timeframe = self._get_timeframe(user_question, init_timeframe)

        with open("src/application/ai_services/prompts/system_prompt.txt", "r", encoding = "utf-8") as f: #system prompt
            raw_system_prompt = f.read()

        system_prompt = raw_system_prompt.format(
            user_query = user_question
        )

        with open("src/application/ai_services/prompts/tools.json", "r", encoding = "utf-8") as f: #tool descriptions
            raw_tools = json.load(f)
        tools = [types.Tool(**t) for t in raw_tools]


        response = self.client.generate_response(tools, system_prompt)

        if response.function_calls:
            f_call = response.function_calls[0]
            f_name = f_call.name
            result = ""

            if f_name == "get_expenses_by_month_markdown":
                result = self.financial_service.get_expenses_by_month_markdown(**f_call.args)

            elif f_name == "get_expenses_by_month_interval_markdown":
                result = self.financial_service.get_expenses_by_month_interval_markdown(**f_call.args)

            elif f_name == "get_expenses_markdown":
                result = self.financial_service.get_expenses_markdown()

            with open("src/application/ai_services/prompts/function_call.txt", "r", encoding="utf-8") as f: #function call response
                raw_function_response = f.read()
            function_response = raw_function_response.format(result=result)
            conversation_history = [system_prompt]

            response = self.client.generate_response(tools, function_response, conversation_history)
            return response.text, timeframe

        return response.text ,timeframe


    def _get_timeframe(self, user_query, init_timeframe): #router for timeframe
        current_date = datetime.now().strftime('%B %Y')

        with open("src/application/ai_services/prompts/tools.json", "r", encoding = "utf-8") as f: #tool descriptions
            raw_tools = json.load(f)
        tools = [types.Tool(**t) for t in raw_tools]

        with open("src/application/ai_services/prompts/router_prompt.txt", "r", encoding = "utf-8") as f: #router prompt
            raw_router_prompt = f.read()



        router_prompt = raw_router_prompt.format(
            current_date = current_date,
            init_timeframe = init_timeframe,
            user_query = user_query
        )

        response = self.client.generate_response(tools, router_prompt)
        return response.text
