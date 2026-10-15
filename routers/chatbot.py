from fastapi import APIRouter, Depends
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.chatbot_service import get_chatbot_reply
from app.utils.security import get_current_user

from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/chatbot",tags=["AI Chatbot"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    
    reply = get_chatbot_reply(request.message,db,current_user.id)

    return ChatResponse(reply=reply,conversation_id=request.conversation_id)