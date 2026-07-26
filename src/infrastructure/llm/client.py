import os
from dotenv import load_dotenv
from google import genai


class Client:

    def __init__(self):
        load_dotenv()
        self.client = genai.Client()

    def generate_response(self, text):
        response = self.client.models.generate_content(
            model = 'gemini-2.5-flash',
            contents = text
        )
        return response.text


