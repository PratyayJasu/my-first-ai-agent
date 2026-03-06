import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .tools import TOOL_FUNCTIONS, TOOL_SCHEMAS
from .prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conversation memory
conversation_history = []


def reset_conversation():
    """Clear the conversation history."""
    global conversation_history
    conversation_history = []


def run_agent(user_input: str, max_iterations: int = 10) -> str:
    """
    Run the agent with the given user input.
    Uses an agentic loop to handle multiple tool calls if needed.
    """
    global conversation_history
    
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Build messages with system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    
    for _ in range(max_iterations):
        # Call the model
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Check if the model wants to call tools
        if assistant_message.tool_calls:
            # Add assistant message with tool calls to history
            messages.append(assistant_message)
            
            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the function
                if function_name in TOOL_FUNCTIONS:
                    try:
                        result = TOOL_FUNCTIONS[function_name](**function_args)
                        tool_result = str(result)
                    except Exception as e:
                        tool_result = f"Error executing {function_name}: {str(e)}"
                else:
                    tool_result = f"Unknown function: {function_name}"
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
        else:
            # No tool calls - we have the final response
            final_response = assistant_message.content
            conversation_history.append({"role": "assistant", "content": final_response})
            return final_response
    
    return "Max iterations reached. Please try rephrasing your request."