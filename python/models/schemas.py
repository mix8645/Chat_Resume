from pydantic import BaseModel

class Query(BaseModel):
    question: str
    session_id: str = "default_session"

class Response(BaseModel):
    question: str
    answer: str
    session_id: str