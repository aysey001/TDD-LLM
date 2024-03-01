from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

task = """I want you to make a list of elements required to create a basic Python program that simulates a simple banking system. 
The program should involve the creation of bank accounts, depositing and withdrawing money, and checking the balance. 
Utilize a class to represent bank accounts and implement functions to perform the specified actions. Additionally, 
create a main loop with a menu to allow users to interact with the banking system, and ensure proper handling of user inputs."""

task2 = """
I want you to create a structure for a system that simulates basic banking operations. 
This system should allow users to establish bank accounts, manage money transactions (deposits and withdrawals), 
and check their account balance. Design a user-friendly main interface with a menu to guide users through the various functionalities, 
and make sure the system can handle user inputs appropriately.
"""

prompt = """Your task is to divide the following coding problem into a numbered list of python tasks, such as imports or function signatures, or classes, required to solve the problem.
Do not write outside the numbered list.
Here is an example:

[INST] I want to input a set of 5 different number into the terminal and the program determines which of those are prime numbers. [/INST]
#Your reply should look like this:
[LIST]
1. get_inputs() # save 5 user inputs into a list of values and returns it
2. calc_prime_number(value)  # calculate the prime numbers from the list of elements and returns a boolean
3. print_prime_number(value, is_prime) # print the prime numbers # takes a value and a boolean and returns the value, if boolean is true
4. main() # use get_inputs() to get the inputs, iterate over the list with calc_prime_number and print_prime_number
[/LIST]
"""


completion = client.chat.completions.create(
  model="",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": task2}
  ]
)

print(completion.choices[0].message.content)