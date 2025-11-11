from agent.prompt import SYSTEM_MESSAGE
from agent.llm import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),  
    ("human", "{query}")      
])

chain = prompt | llm | parser

query = input("Ask my agent: ")

response = chain.invoke({"query": query})
print(response)