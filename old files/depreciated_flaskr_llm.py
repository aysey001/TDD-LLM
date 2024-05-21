from langchain_openai import ChatOpenAI

from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

from testers.lintingTest import lintingTest
from testers.tagHandler import tagHandler

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

#builds the prompt from the files in the prompt folder, leaves final input empty for chaining.
def get_prompt(type:str, stage:str):
    examples = [{
        "input": read_file("prompt//"+ type +"//"+ type +"_"+ stage +"_input.txt") , 
        "output": read_file("prompt//"+ type +"//"+ type +"_"+ stage +"_output.txt")
    }]

    #simple chat prompt with input and output
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    
    #few shot prompt with examples
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    #generates few shot prompt with examples from files
    prompt = ChatPromptTemplate.from_messages(
        [
            #simplify by using name + _system_message.txt
            ("system", read_file("prompt//system_message//system_message_" + stage + ".txt")),
            few_shot_prompt,
            ("human", "{input}")
        ]
    )
    return prompt

def main():
    # connect to the local server
    llm = ChatOpenAI(openai_api_key="not needed", openai_api_base="http://localhost:8000/v1")

    #customize the prompt type and user message
    #potential commandline arguments
    # get user message, files are in user_message folder
    set_type = "flaskr"
    user_message_path = "prompt//user_message//plantmanager.txt"
    user_message = read_file(user_message_path)

    # get the outline prompt, files are in prompt folder
    # chain the outline prompt with the language model
    # invoke the chain with the input from the user
    outline_prompt = get_prompt( type=set_type, stage="outline")
    outline_chain = outline_prompt | llm
    outline = outline_chain.invoke({"input": user_message} )
    print(outline.content)

    # same for tests
    tests_prompt = get_prompt(type=set_type, stage="test")
    tests_chain = tests_prompt | llm
    tests = tests_chain.invoke({"input": outline.content} )
    print(tests.content)
    
    # same for code
    code_prompt = get_prompt(type=set_type, stage="code")
    code_chain = code_prompt | llm
    code = code_chain.invoke({"input": tests.content} )
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
    
    if res == False:
        print("Could not repair.")
    else:
        print("done!")
    
    if input("Do you want to save the code? (y/n)") == "y":
        tagHandler_result = tagHandler(repair.content)
        final_code = tagHandler_result.remove_python_tags()
        with open("result.py", "w") as file:
            file.write(final_code)
            print("Code saved as output.py")

main()