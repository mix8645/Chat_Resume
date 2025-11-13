from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from agent.prompt import SYSTEM_MESSAGE
from agent.llm import llm
from tasks.vector_storage import retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

app = FastAPI(title="Resume Chat Agent API")

# Bearer Token Security
security = HTTPBearer()

# Get API token from environment variable
API_TOKEN = os.getenv("API_TOKEN")

# Authentication function
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Setup RAG chain
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE + "\n\nContext:\n{context}"),
    ("human", "{query}"),
])

rag_chain = (
    {"context": retriever, "query": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

# Pydantic models
class Query(BaseModel):
    question: str

class Response(BaseModel):
    question: str
    answer: str

# Public endpoint (no auth required)
@app.get("/")
def read_root():
    return {
        "message": "Resume Chat Agent API is running!",
        "version": "0.1.0",
        "endpoints": {
            "ask": "/ask (POST, requires Bearer token)",
            "health": "/health (GET, public)"
        }
    }

# Health check endpoint (no auth required)
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Protected endpoint (requires Bearer token)
@app.post("/ask", response_model=Response)
def ask_question(
    query: Query, 
    token: str = Depends(verify_token)
):
    """
    Ask a question about the resume. Requires Bearer token authentication.
    """
    try:
        response = rag_chain.invoke(query.question)
        return Response(question=query.question, answer=response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)