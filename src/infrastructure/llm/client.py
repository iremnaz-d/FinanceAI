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
             self.client = genai.Client()

    def generate_response(self, tools, text, history = None):

        if self.client is None:
            raise ValueError("Gemini API Key not found.")


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


