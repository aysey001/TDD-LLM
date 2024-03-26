import sys

from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

from testers.lintingTest import lintingTest
from testers.tagHandler import tagHandler
from testers.listdivider import split_string
from testers.promptbuilder import get_prompt
from testers.fileaccess import read_file, write_file




#builds the prompt from the files in the prompt folder, leaves final input empty for chaining.


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

    if (custom_outline == False):
        # get the outline prompt, files are in prompt folder
        # chain the outline prompt with the language model
        # invoke the chain with the input from the user
        outline_prompt = get_prompt( type=set_type, stage="outline")
        outline_chain = outline_prompt | llm
        outline = outline_chain.invoke({"input": user_message} )
        outline_text = outline.content
        print(outline.content)
        write_file("result_outline.txt", outline.content)
    else:
        outline_text = read_file("result_outline.txt")


    #loop through the outline and generate tests and code outline is reduced by pop()
    outline_list = split_string(outline_text)
    while(outline_list):
        # same for tests
        test_prompt = get_prompt(type=set_type, stage="test")
        test_chain = test_prompt | llm
        test = test_chain.invoke({"input": "[INST]\n" + outline_list.pop() + "\n[/INST]" } )
        test_increment = test.content
        test_string += test_increment
        print(test.content)
    
        # same for code
        code_prompt = get_prompt(type=set_type, stage="code")
        code_chain = code_prompt | llm
        code = code_chain.invoke({"input": test_increment} )
        code_increment = code.content
        code_string += code_increment
        print(code.content)

        #check for correct tags and linting
        tagHandler_code = tagHandler(code.content)
        lintingTest_code = lintingTest(tagHandler_code.remove_python_tags())
        res = lintingTest_code.run_lint()
        if res: 
            print("no errors in linting")
        #repair code if necessary. max tries = 3
        repair_count = 1
        while res==False and repair_count <= 3:
            #print "Error occured. repairing... 1/3"
            print("Error in Code. repairing... " + str(repair_count) + "/3")
        
            #same as before, but with repair prompt
            repair_prompt = get_prompt(type=set_type, stage="repair")
            repair_chain = repair_prompt | llm
            repair = repair_chain.invoke({"input": code.content} )
            print(repair.content)
        
            tagHandler_repair = tagHandler(repair.content)
            lintingTest_repair = lintingTest(tagHandler_repair.remove_python_tags())
            res = lintingTest_repair.run_lint()

            repair_count += 1
    
        full_repaired_code += lintingTest_code.text+"\n"
        full_test_code += lintingTest_repair.text+"\n"

        if res == False:
            print("Could not repair.")
    
    if input("Do you want to save the code? (y/n)") == "y":
        write_file("result_code.py", full_repaired_code)
        write_file("result_tests.py", full_test_code)
main()