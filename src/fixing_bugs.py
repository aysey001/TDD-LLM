from langchain_openai import ChatOpenAI
import sys

from testers.lintingTest import lintingTest
from testers.tagHandler import tagHandler
from testers.listdivider import split_string
from testers.promptbuilder import get_prompt
from testers.fileaccess import read_file, write_file

from langchain.prompts import (ChatPromptTemplate)

def main():
    # connect to the local server
    llm = ChatOpenAI(openai_api_key="not needed", openai_api_base="http://localhost:8000/v1")

    #generates few shot prompt with examples from files
    outline_prompt = (
        [
            #simplify by using name + _system_message.txt
            ("system", read_file("prompt//system_message//system_message_outline.txt")),
            ("human", read_file("prompt//user_message//plantmanager.txt")),
        ]
    )


    write_file("test.txt",llm.invoke(outline_prompt).content)

def split_test():
    # connect to the local server
    llm = ChatOpenAI(openai_api_key="not needed", openai_api_base="http://localhost:8000/v1")

    test_prompt = (
        [
            #simplify by using name + _system_message.txt
            ("system", read_file("prompt//system_message//system_message_test.txt")),
            ("human", "{input}"),
        ]
    )

    outline_with_tags = read_file("test.txt")
    outline_without_tags = tagHandler(outline_with_tags).remove_list_tags()
    #print(outline_without_tags) works
    outline_list = split_string(outline_without_tags)
    while(outline_list):
        
        outline_increment=outline_list.pop(0)
        test_increment = llm.invoke(test_prompt, {"input": outline_increment}).content
        print(test_increment)


split_test()