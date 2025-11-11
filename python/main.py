from agent.prompt import SYSTEM_MESSAGE
from agent.llm import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),  
    ("human", "{question}")      
])

chain = prompt | llm | parser

response = chain.invoke({"question":"How many experince he got?"})
print(response)