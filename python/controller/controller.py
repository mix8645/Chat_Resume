from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas import Query, Response
from auth.security import verify_token

from agent.rag_chain import rag_chain
from tasks.history_manage import chat_history

router = APIRouter()

@router.get("/")
def read_root():
    return {
        "message": "Resume Chat Agent API is running!",
        "version": "0.1.0",
        "endpoints": {
            "ask": "/ask (POST, requires Bearer token)",
            "health": "/health (GET, public)"
        }
    }

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/ask", response_model=Response)
def ask_question(
    query: Query, 
    token: str = Depends(verify_token)
):
    """
    Ask a question about the resume. Requires Bearer token authentication.
    """
    try:
        result = rag_chain.invoke({
            "input": query.question,
            "chat_history": chat_history
        })
        
        # Add to chat history
        chat_history.append(("human", query.question))
        chat_history.append(("ai", result["answer"]))
        
        return Response(question=query.question, answer=result["answer"])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )