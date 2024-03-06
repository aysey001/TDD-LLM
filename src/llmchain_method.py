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
def get_prompt(name):
    examples = [
        {"input": read_file("prompt//" + name + "_input.txt") , "output": read_file("prompt//" + name + "_output.txt")},
    ]

    #simple chat prompt with input and output
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    #generates few shot prompt with examples from files
    prompt = ChatPromptTemplate.from_messages(
        [
            #simplify by using name + _system_message.txt
            ("system", read_file("prompt//" + "system_message_" + name + ".txt")),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    return prompt



def main():
    # connect to the local server
    llm = ChatOpenAI(openai_api_key="not needed",openai_api_base="http://localhost:8000/v1")

    # get the outline prompt, files are in prompt folder
    outline_prompt = get_prompt("outline")
    # chain the outline prompt with the language model
    outline_chain = outline_prompt | llm
    # invoke the chain with the input from the user
    outline = outline_chain.invoke({"input": read_file("prompt//user_message.txt")} )
    print(outline.content)

    # same for tests and code
    tests_prompt = get_prompt("tests")
    tests_chain = tests_prompt | llm
    tests = tests_chain.invoke({"input": outline.content} )
    print(tests.content)
    
    code_prompt = get_prompt("code")
    code_chain = code_prompt | llm
    code = code_chain.invoke({"input": tests.content} )
    print(code.content)

    #check for correct tags and linting
    tH = tagHandler(code.content)
    lT = lintingTest(tH.remove_python_tags())
    res = lT.run_lint()
    
    #repair code if necessary. max tries = 3
    repair_count = 1
    while res==False and repair_count <= 3:
        #print "Error occured. repairing... 1/3"
        print("Error in Code. repairing... " + str(repair_count) + "/3")
        
        #same as before, but with repair prompt
        repair_prompt = get_prompt("repair")
        repair_chain = repair_prompt | llm
        repair = repair_chain.invoke({"input": code.content} )
        print(repair.content)
        repair_count += 1
    
    if res == False:
        print("Could not repair.")
    else:
        print("done!")

main()