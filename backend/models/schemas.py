from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for sending a chat message."""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What time is it?"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    response: str
    conversation_length: int
    timestamp: datetime = None
    
    def __init__(self, **data):
        if data.get("timestamp") is None:
            data["timestamp"] = datetime.now()
        super().__init__(**data)
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The current time is Friday, March 10, 2026 at 14:30:00",
                "conversation_length": 2,
                "timestamp": "2026-03-10T14:30:00"
            }
        }


class Message(BaseModel):
    """A single message in the conversation."""
    role: str
    content: str


class ConversationHistory(BaseModel):
    """The full conversation history."""
    messages: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi! How can I help you?"}
                ]
            }
        }


class ToolInfo(BaseModel):
    """Information about an available tool."""
    name: str
    description: str
    parameters: Dict[str, Any]
