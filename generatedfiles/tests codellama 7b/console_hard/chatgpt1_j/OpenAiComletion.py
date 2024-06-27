import os
import requests

class OpenAiCompletion:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {"Authorization": "Bearer " + self.api_key}

    def complete(self, prompt):
        response = requests.post(self.base_url + "/engines/content-filter-alpha/completions", headers=self.headers, json={"prompt": prompt, "max_tokens": 5})
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()