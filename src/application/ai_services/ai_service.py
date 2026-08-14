from src.application.financial_services import FinancialService
from src.infrastructure.llm.client import Client
from datetime import datetime
import json
from google.genai import types


class AIService:

    def __init__(self, provided_api_key = None):
        if provided_api_key:
            self.client = Client(provided_api_key = provided_api_key)
        else:
            self.client = Client() #if provided_api_key does not exist, initiating Client with the api key from .env

        self.financial_service = FinancialService()


    def get_financial_insight(self, user_question, init_timeframe):
        """
        The main method that receives a response from artificial intelligence
        :param user_question: user's question
        :param init_timeframe: recently asked timeframe
        :return: Gemini's response, last asked timeframe
        """
        current_date = datetime.now().strftime('%B %Y')

        with open("src/application/ai_services/prompts/system_prompt.txt", "r", encoding = "utf-8") as f: #system prompt
            raw_system_prompt = f.read()

        system_prompt = raw_system_prompt.format(
            current_date = current_date,
            user_query = user_question,
            timeframe = init_timeframe
        )

        with open("src/application/ai_services/prompts/tools.json", "r", encoding = "utf-8") as f: #tool descriptions
            raw_tools = json.load(f)
        tools = [types.Tool(**t) for t in raw_tools]


        response = self.client.generate_response(tools, system_prompt)

        new_timeframe = init_timeframe

        if response.function_calls: # if there is a function call
            f_call = response.function_calls[0]
            f_name = f_call.name
            args = f_call.args if f_call.args else {} # arguments of the required function
            result = ""

            if f_name == "get_expenses_by_month_markdown":
                month = args.get("month", "")
                year = args.get("year", "")
                new_timeframe = f"{month} {year}".strip()
                result = self.financial_service.get_expenses_by_month_markdown(**f_call.args)

            elif f_name == "get_expenses_by_month_interval_markdown":
                fm = args.get("first_month", "")
                fy = args.get("first_year", "")
                sm = args.get("second_month", "")
                sy = args.get("second_year", "")
                new_timeframe = f"{fm} {fy} {sm} {sy}".strip()
                result = self.financial_service.get_expenses_by_month_interval_markdown(**f_call.args)

            elif f_name == "get_expenses_markdown":
                new_timeframe = 'ALL'
                result = self.financial_service.get_expenses_markdown()

            with open("src/application/ai_services/prompts/function_call.txt", "r", encoding="utf-8") as f: #function call response
                raw_function_response = f.read()
            function_response = raw_function_response.format(result=result)
            conversation_history = [system_prompt]

            # getting the main response by sending system prompt with the function call result
            response = self.client.generate_response(tools, function_response, conversation_history)
            return response.text, new_timeframe

        return response.text ,new_timeframe
