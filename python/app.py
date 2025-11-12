from agent.prompt import SYSTEM_MESSAGE
from agent.llm import llm
from tasks.vector_storage import retriever

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),
    ("context", "{context}"),
    ("human", "{query}"),
])

rag_chain = (
    {"context" : retriever, "query" : RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

query = input("Ask my agent: ")

response = rag_chain.invoke(query)
print(response)