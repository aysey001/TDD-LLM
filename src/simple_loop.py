from langchain_openai import ChatOpenAI
import sys

from prompthandle.lintingTest import lintingTest
from prompthandle.tagHandler import tagHandler
from prompthandle.promptbuilder import get_prompt
from prompthandle.fileaccess import read_file, write_file



## prepare
# settings
entry_point = "test"
stop_point = "code"
example_type = "flaskr"
user_message_path = "prompt//user_message//ocpl.txt"
# connect to llm
llm = ChatOpenAI(openai_api_key="not needed", openai_api_base="http://localhost:8000/v1")


# get prompts (outline, test, code, repair) and  prepare chains
outline_prompt = get_prompt( type=example_type, stage="outline")
outline_chain = outline_prompt | llm
test_prompt = get_prompt( type=example_type, stage="test")
test_chain = test_prompt | llm
code_prompt = get_prompt( type=example_type, stage="code")
code_chain = code_prompt | llm
repair_prompt = get_prompt( type=example_type, stage="repair")
repair_chain = repair_prompt | llm


# invoke the outline chain with the input from the user or get outline from file
if entry_point == "new":
    # get user_message
    user_message = read_file(user_message_path)
    print("generating outline...")
    outline = outline_chain.invoke({"input": user_message} )
    outline_message = outline.content
    write_file("results//results_outline.txt", outline_message)
    print("outline generated under results/results_outline!")
elif entry_point == "outline":
    outline_message = read_file("entry_point//entry_point_outline.txt")
    print("outline has been read from entry_point/entry_point_outline")

# stop if stop_point is outline
if stop_point == "outline":
    print("stop point outline reached! stopping!")
    sys.exit()

# invoke the test chain with outline or get test from file
if entry_point == "new" or entry_point == "outline":
    print ("generating test...")
    test = test_chain.invoke({"input": outline_message})
    test_message = test.content
    write_file("results//results_test.txt", test_message)
    print("test generated under results/results_test!")
elif entry_point == "test":
    test_message = read_file("entry_point//entry_point_test.txt")
    print("test has been read from entry_point/entry_point_test")

# stop if stop_point is test
if stop_point == "test":
    print("stop point test reached! stopping!")
    sys.exit()

# invoke the code chain with test or get code from file
if entry_point == "new" or entry_point == "outline" or entry_point == "test":
    print ("generating code...")
    code = code_chain.invoke({"input": test_message})
    code_message = code.content
    write_file("results//results_code_unverified.txt", code_message)
    print("code generated under results/results_code_unverified!")
elif entry_point == "code":
    code_message = read_file("entry_point//entry_point_code.txt")
    print("code has been read from entry_point/entry_point_code")

#stop if stop_point is code
if stop_point == "code":
    print("stop point code reached! stopping!")
    sys.exit()

# remove tags, lint the code and write to file if successful
tagless_code = tagHandler(code_message).remove_python_tags()
linting_result = lintingTest(tagless_code).run_lint()
if linting_result == True:
    print("code linted successfully")
    write_file("results//results_code_success.txt", code_message)
    sys.exit()
else:
    print("linting failed")
    write_file("results//results_code_lint_failed.txt", code_message)

# while linting fails, attempt to repair the code
attempts = 1
while linting_result == False and attempts <= 3:
    
    # invoke the repair chain with the code
    print("attempting to repair code... " + str(attempts) + "/3 attempts")
    repair = repair_chain.invoke({"input": code_message})
    repair_message = repair.content
    write_file("results//results_code_repair_"+ str(attempts) +".txt", repair_message)
    # remove tags, lint the repaired code and write to file if successful
    tagless_repair = tagHandler(repair_message).remove_python_tags()
    linting_result = lintingTest(tagless_repair).run_lint()
    # if linting is successful, write to file and exit
    if linting_result == True:
        print("repaired code linted successfully")
        write_file("results//results_code_success.txt", repair_message)
        sys.exit()
    else:
        attempts += 1

if attempts == 4:
    print("repair failed after 3 attempts")
    sys.exit()





