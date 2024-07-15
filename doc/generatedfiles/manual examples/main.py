from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

task = """<<SYS>>
You are a helpful coding assistant.
Write a function that implements a list of requirements as python code.
<</SYS>>"""

prompt = """[INST]
1. name it `save_user_info`
2. takes in 2 parameters: `name` and `age`
3. returns a string in the following format: "Hello, my name is 'name' and I am 'age' years old"
4. if `name` is not a string, raise a `TypeError` with the message "name must be a string"
5. if `age` is not an integer, raise a `TypeError` with the message "age must be an integer"
6. if `age` is less than 0, raise a `ValueError` with the message "age must be a positive integer"
[/INST]
"""


completion = client.chat.completions.create(
  model="",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": task}
  ]
)

print(completion.choices[0].message.content)