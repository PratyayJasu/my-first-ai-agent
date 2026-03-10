from typing import List, Optional
from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse, ConversationHistory, ToolInfo
from agent.agent import run_agent, reset_conversation, get_conversation_history
from agent.tools import TOOL_FUNCTIONS, TOOL_SCHEMAS

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the AI assistant and get a response."""
    try:
        response = run_agent(request.message)
        history = get_conversation_history()
        return ChatResponse(
            response=response,
            conversation_length=len(history)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=ConversationHistory)
async def get_history():
    """Get the current conversation history."""
    history = get_conversation_history()
    return ConversationHistory(messages=history)


@router.delete("/history")
async def clear_history():
    """Clear the conversation history."""
    reset_conversation()
    return {"message": "Conversation history cleared"}


@router.get("/tools", response_model=List[ToolInfo])
async def list_tools():
    """List all available tools."""
    tools = []
    for schema in TOOL_SCHEMAS:
        func = schema["function"]
        tools.append(ToolInfo(
            name=func["name"],
            description=func.get("description", ""),
            parameters=func.get("parameters", {}).get("properties", {})
        ))
    return tools
