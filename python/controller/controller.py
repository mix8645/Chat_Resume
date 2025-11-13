from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas import Query, Response
from auth.security import verify_token

from agent.rag_chain import conversational_rag_chain
from tasks.history_manage import store

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
    token: str = Depends(verify_token),
):
    """
    Ask a question about the resume. Requires Bearer token authentication.
    """
    try:
        result = conversational_rag_chain.invoke(
            {"input": query.question},
            config={"configurable": {"session_id": query.session_id}}
        )
        
        answer = result.get("answer", "")
        
        return Response(
            question=query.question, 
            answer=answer,
            session_id=query.session_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )
        
@router.get("/history/{session_id}")
def get_history(session_id: str, token: str = Depends(verify_token)):
    """
    Get chat history for a specific session.
    """    
    if session_id not in store:
        return {
            "session_id": session_id,
            "message_count": 0,
            "messages": []
        }
    
    history = store[session_id]
    messages = [
        {
            "type": msg.type,
            "content": msg.content
        }
        for msg in history.messages
    ]
    
    return {
        "session_id": session_id,
        "message_count": len(messages),
        "messages": messages
    }

# Clear chat history for a session
@router.delete("/history/{session_id}")
def clear_history(session_id: str, token: str = Depends(verify_token)):
    """
    Clear chat history for a specific session.
    """
    if session_id in store:
        store[session_id].clear()
        return {
            "message": f"History cleared for session {session_id}",
            "success": True
        }
    
    return {
        "message": f"No history found for session {session_id}",
        "success": False
    }