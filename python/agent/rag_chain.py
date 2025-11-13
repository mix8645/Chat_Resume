from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from agent.prompt import SYSTEM_MESSAGE, HISTORY_SYSTEM_MESSAGE
from agent.llm import llm
from tasks.vector_storage import retriever
from tasks.history_manage import get_session_history

# Setup prompts
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", HISTORY_SYSTEM_MESSAGE),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create history-aware retriever
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# QA prompt
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE + "\n\nContext:\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create document chain
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Create RAG chain
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key = "input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)