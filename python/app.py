from agent.prompt import SYSTEM_MESSAGE
from agent.llm import llm
from tasks.vector_storage import retriever

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE + "\n\nContext:\n{context}"),
    ("human", "{query}"),
])

rag_chain = (
    {"context" : retriever, "query" : RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

while True:
    query = input("Ask my agent: ")
    
    if query.lower() == 'exit':
        print("Exiting...")
        break

response = rag_chain.invoke(query)
print(retriever)
print(response)