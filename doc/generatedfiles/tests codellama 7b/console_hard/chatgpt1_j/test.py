import unittest
from openai import OpenAiCompletion

class TestOpenAiCompletion(unittest.TestCase):

    def test_openai_completion(self):
        api_key = ""
        client = OpenAiCompletion(api_key)
        prompt = "This is a test prompt"
        completion = client.complete(prompt)
        self.assertIsInstance(completion, str)
        self.assertTrue(len(completion) > 0)

if __name__ == '__main__':
    unittest.main()