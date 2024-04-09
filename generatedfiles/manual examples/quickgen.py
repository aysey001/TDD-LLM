from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

prompt= "generate a quick python example"
task= "write me a short python program"
completion = client.chat.completions.create(
  model="",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": task}
  ]
)

print(completion.choices[0].message.content)