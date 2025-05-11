import json
import os

import google.generativeai as genai

from singleton import Singleton


class Gemini(metaclass=Singleton):
    def __init__(self):
        self.base_directory = str(os.path.expanduser('~/GPT-Writer/'))
        with open(f'{self.base_directory}config', 'r') as json_file:
            config = json.load(json_file)
            self.GOOGLE_API_KEY = config['AI_API_KEY']
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.geminiModel = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, prompt):
        return self.geminiModel.generate_content(prompt).text
