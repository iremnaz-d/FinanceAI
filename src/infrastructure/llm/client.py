from dotenv import load_dotenv
from google import genai
from google.genai import types


class Client:

    def __init__(self):
        load_dotenv()
        self.client = genai.Client()

    def generate_response(self, tools,text):
        response = self.client.models.generate_content(
            model = 'gemini-3.6-flash',
            contents = text,
            config = types.GenerateContentConfig(
                tools = tools
            )
        )
        return response


