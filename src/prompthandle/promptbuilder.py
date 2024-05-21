from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

from prompthandle.fileaccess import read_file

#builds the prompt from the files in the prompt folder, leaves final input empty for chaining.
def get_prompt(type:str,stage:str):
    examples = [
        {"input": read_file("prompt//"+ type +"//"+ type +"_"+ stage +"_input.txt") ,
            "output": read_file("prompt//"+ type +"//"+ type +"_"+ stage +"_output.txt")},
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
            ("system", read_file("prompt//system_message//" + "system_message_" + stage + ".txt")),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )
    return prompt