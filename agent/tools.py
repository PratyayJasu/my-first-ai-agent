import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import requests
from duckduckgo_search import DDGS

# Directory for storing notes
NOTES_DIR = Path(__file__).resolve().parent.parent / "data" / "notes"
NOTES_DIR.mkdir(parents=True, exist_ok=True)


# ============== Tool Functions ==============

def get_current_datetime() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S")


def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    # Only allow safe characters for math
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: Invalid characters in expression. Only numbers and +-*/.() allowed."
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def web_search(query: str, num_results: int = 5) -> str:
    """Search the web using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
        
        if not results:
            return "No results found."
        
        output = []
        for i, r in enumerate(results, 1):
            output.append(f"{i}. {r['title']}\n   {r['href']}\n   {r['body'][:150]}...")
        
        return "\n\n".join(output)
    except Exception as e:
        return f"Search error: {str(e)}"


def fetch_webpage(url: str) -> str:
    """Fetch and return the text content of a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AIAgent/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Simple extraction - just get text, limit size
        from html.parser import HTMLParser
        
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False
            
            def handle_starttag(self, tag, attrs):
                if tag in ('script', 'style', 'nav', 'header', 'footer'):
                    self.skip = True
            
            def handle_endtag(self, tag):
                if tag in ('script', 'style', 'nav', 'header', 'footer'):
                    self.skip = False
            
            def handle_data(self, data):
                if not self.skip:
                    text = data.strip()
                    if text:
                        self.text.append(text)
        
        parser = TextExtractor()
        parser.feed(response.text)
        content = " ".join(parser.text)
        
        # Limit content length
        if len(content) > 3000:
            content = content[:3000] + "... [truncated]"
        
        return content
    except Exception as e:
        return f"Error fetching page: {str(e)}"


def save_note(title: str, content: str) -> str:
    """Save a note to a file."""
    # Sanitize filename
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    filename = NOTES_DIR / f"{safe_title}.txt"
    
    try:
        with open(filename, "w") as f:
            f.write(f"Title: {title}\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 40 + "\n")
            f.write(content)
        return f"Note saved: {safe_title}.txt"
    except Exception as e:
        return f"Error saving note: {str(e)}"


def read_note(title: str) -> str:
    """Read a note by title."""
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    filename = NOTES_DIR / f"{safe_title}.txt"
    
    if not filename.exists():
        # Try to find partial match
        matches = list(NOTES_DIR.glob(f"*{safe_title}*"))
        if matches:
            filename = matches[0]
        else:
            return f"Note not found: {title}"
    
    try:
        with open(filename, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading note: {str(e)}"


def list_notes() -> str:
    """List all saved notes."""
    notes = list(NOTES_DIR.glob("*.txt"))
    if not notes:
        return "No notes found."
    
    output = ["Saved notes:"]
    for note in notes:
        output.append(f"  - {note.stem}")
    return "\n".join(output)


def delete_note(title: str) -> str:
    """Delete a note by title."""
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    filename = NOTES_DIR / f"{safe_title}.txt"
    
    if not filename.exists():
        return f"Note not found: {title}"
    
    try:
        filename.unlink()
        return f"Note deleted: {title}"
    except Exception as e:
        return f"Error deleting note: {str(e)}"


def run_shell_command(command: str) -> str:
    """Run a shell command and return the output. Use with caution."""
    # Block dangerous commands
    dangerous = ['rm -rf', 'sudo', 'mkfs', 'dd', '> /dev', 'chmod 777']
    if any(d in command.lower() for d in dangerous):
        return "Error: This command is not allowed for safety reasons."
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout or result.stderr or "Command completed with no output."
        if len(output) > 2000:
            output = output[:2000] + "... [truncated]"
        return output
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error: {str(e)}"


# ============== Function Registry ==============

TOOL_FUNCTIONS = {
    "get_current_datetime": get_current_datetime,
    "calculate": calculate,
    "web_search": web_search,
    "fetch_webpage": fetch_webpage,
    "save_note": save_note,
    "read_note": read_note,
    "list_notes": list_notes,
    "delete_note": delete_note,
    "run_shell_command": run_shell_command,
}


# ============== OpenAI Tool Schemas ==============

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Supports +, -, *, /, parentheses, and decimal numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '(2 + 3) * 4.5'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information using DuckDuckGo",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_webpage",
            "description": "Fetch and extract text content from a webpage URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Save a note with a title and content for later reference",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title/name of the note"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content of the note"
                    }
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "Read a previously saved note by its title",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the note to read"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List all saved notes",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_note",
            "description": "Delete a saved note by its title",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the note to delete"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell_command",
            "description": "Run a shell command and return the output. Use for system tasks like listing files, checking disk space, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run"
                    }
                },
                "required": ["command"]
            }
        }
    }
]
