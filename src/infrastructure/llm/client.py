from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

class Client:

    def __init__(self, provided_api_key = None):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY") or provided_api_key

        if not api_key:
            self.client = None
        else:
             self.client = genai.Client(api_key = api_key)

    def generate_response(self, tools, text, history = None):
        """
        :param tools: Function descriptions to make Function Call
        :param text: User command
        :param history: User command history as list, if needed
        :return: response
        """

        if self.client is None:
            raise ValueError("Gemini API Key not found.")

        # “history” is generally used when a function call is made to send both the initial
        # command and the result of the function call to the LLM
        if history is None:
            history = [text]
        else:
            history.append(text)

        response = self.client.models.generate_content(
            model = 'gemini-3.6-flash',
            contents = history,
            config = types.GenerateContentConfig(
                tools = tools
            )
        )
        return response