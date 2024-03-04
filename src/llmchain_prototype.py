from langchain_openai import ChatOpenAI

from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

llm = ChatOpenAI(openai_api_key="not needed",openai_api_base="http://localhost:8000/v1")

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    

initial_message= """[INST] Write a very simple console app for a banking system. [/INST]"""

outline_examples = [
    {"input": read_file("outline_input.txt") , "output": read_file("outline_output.txt")},
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

outline_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=outline_examples,
)

outline_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", read_file("system_message_outline.txt")),
        outline_few_shot_prompt,
        ("human", "{input}"),
    ]
)

outline_chain = outline_prompt | llm
outline = outline_chain.invoke({"input": initial_message} )
print(outline.content)


tests_examples = [
    {"input": read_file("tests_input.txt") , "output": read_file("tests_output.txt")},
]

tests_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=tests_examples,
)

tests_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", read_file("system_message_tests.txt")),
        tests_few_shot_prompt,
        ("human", "{input}"),
    ]
)

tests_chain = tests_prompt | llm
tests = tests_chain.invoke({"input": outline.content})
print(tests.content)


code_examples = [
    {"input": read_file("code_input.txt") , "output": read_file("code_output.txt")},
]

code_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=code_examples,
)

code_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", read_file("system_message_code.txt")),
        code_few_shot_prompt,
        ("human", "{input}"),
    ]
)

code_chain = code_prompt | llm
code = code_chain.invoke({"input": tests.content})
print(code.content)


