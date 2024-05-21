from langchain_openai import ChatOpenAI
import sys

from testers.lintingTest import lintingTest
from testers.tagHandler import tagHandler
from testers.listdivider import split_string
from testers.promptbuilder import get_prompt
from testers.fileaccess import read_file, write_file

def main():
    # connect to the local server
    llm = ChatOpenAI(openai_api_key="not needed", openai_api_base="http://localhost:8000/v1")

    #customize the prompt type and user message
    #potential commandline arguments
    # get user message, files are in user_message folder
    set_type = "flaskr"
    user_message_path = "prompt//user_message//plantmanager.txt"
    user_message = read_file(user_message_path)
    custom_outline = False

    #setup llms
    outline_prompt = get_prompt( type=set_type, stage="outline")
    outline_chain = outline_prompt | llm

    test_prompt = get_prompt(type=set_type, stage="test")
    test_chain = test_prompt | llm

    code_prompt = get_prompt(type=set_type, stage="code")
    code_chain = code_prompt | llm

    repair_prompt = get_prompt(type=set_type, stage="repair")
    repair_chain = repair_prompt | llm

    test_string =  ""
    code_string = ""

    if (custom_outline == False):
        # get the outline prompt, files are in prompt folder
        # chain the outline prompt with the language model
        # invoke the chain with the input from the user
        outline = outline_chain.invoke({"input": user_message})
        outline_text = outline.content
        print(outline.content)
        outline_cleaned = tagHandler(outline_text).remove_list_tags()
        write_file("result_outline.txt", outline_cleaned)
    else:
        outline_text = read_file("result_outline.txt")


    outline_list = split_string(outline_cleaned)
    for outline_element in outline_list:
        outline_element = "[INST]\n" + outline_element + "\n[/INST]"
        print(outline_element)

    while(outline_list):

        test = test_chain.invoke({"input": outline_list.pop(0)})
        test_increment = test.content
        print(test_increment)
        
        code = code_chain.invoke({"input": test_increment})
        code_increment = code.content
        print(code_increment)

        test_string += tagHandler(test_increment).remove_tests_tags()
        
        
        res= lintingTest(code_string).run_lint() == False
        attempt = 1

        while(res == False and attempt <= 3):
            print("Error in Code. repairing... " + str(attempt) + "/3")
            repair = repair_chain.invoke({"input": code_increment})
            repair_increment = repair.content
            res = lintingTest(repair_increment).run_lint()
            attempt += 1
            #NEW FEATURE: pass the unittest here 
        
            if (res == True):
                print("no errors in linting")
                code_increment = repair_increment
            else:
                print("repair attempt failed")
        
        code_string += tagHandler(code_increment).remove_python_tags()

    write_file("result_tests.txt", test_string)
    write_file("result_code.txt", code_string)

main()
