import sys
import threading
import time
from agent.agent import run_agent, reset_conversation


# ============== Colors ==============

class Colors:
    """ANSI color codes for terminal output."""
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def colored(text: str, color: str) -> str:
    """Wrap text with color codes."""
    return f"{color}{text}{Colors.RESET}"


# ============== Loading Spinner ==============

class Spinner:
    """Simple loading spinner for long operations."""
    def __init__(self, message="Thinking"):
        self.message = message
        self.running = False
        self.thread = None
    
    def _spin(self):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while self.running:
            sys.stdout.write(f"\r{colored(self.message, Colors.DIM)} {chars[i % len(chars)]} ")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()


# ============== Help Text ==============

HELP_TEXT = f"""
{colored("Available Commands:", Colors.BOLD + Colors.CYAN)}

  {colored("/help", Colors.YELLOW)}     Show this help message
  {colored("/clear", Colors.YELLOW)}    Clear conversation history
  {colored("/tools", Colors.YELLOW)}    List available tools
  {colored("exit", Colors.YELLOW)}      Quit the agent

{colored("Available Tools:", Colors.BOLD + Colors.CYAN)}

  {colored("get_current_datetime", Colors.GREEN)}  Get current date and time
  {colored("calculate", Colors.GREEN)}             Evaluate math expressions
  {colored("web_search", Colors.GREEN)}            Search the web (DuckDuckGo)
  {colored("fetch_webpage", Colors.GREEN)}         Get content from a URL
  {colored("save_note", Colors.GREEN)}             Save a note
  {colored("read_note", Colors.GREEN)}             Read a saved note
  {colored("list_notes", Colors.GREEN)}            List all notes
  {colored("delete_note", Colors.GREEN)}           Delete a note
  {colored("run_shell_command", Colors.GREEN)}     Run shell commands

{colored("Examples:", Colors.BOLD + Colors.CYAN)}

  "What time is it?"
  "Search for Python tutorials"
  "Save a note called shopping with content: milk, eggs, bread"
  "Calculate 15% of 250"
  "List files in the current directory"
"""

TOOLS_TEXT = f"""
{colored("Available Tools:", Colors.BOLD + Colors.CYAN)}

  {colored("get_current_datetime", Colors.GREEN)}
    Get the current date and time
    Example: "What time is it?"

  {colored("calculate", Colors.GREEN)}
    Evaluate mathematical expressions
    Example: "Calculate (25 * 4) / 2"

  {colored("web_search", Colors.GREEN)}
    Search the web using DuckDuckGo
    Example: "Search for latest Python news"

  {colored("fetch_webpage", Colors.GREEN)}
    Extract text content from a URL
    Example: "Fetch https://example.com"

  {colored("save_note / read_note / list_notes / delete_note", Colors.GREEN)}
    Manage personal notes
    Example: "Save a note called todo with content: finish project"

  {colored("run_shell_command", Colors.GREEN)}
    Execute shell commands (with safety restrictions)
    Example: "List files in current directory"
"""


# ============== Main ==============

def print_banner():
    """Print welcome banner."""
    banner = f"""
{colored("╔════════════════════════════════════════╗", Colors.CYAN)}
{colored("║", Colors.CYAN)}    {colored("🤖 AI Assistant", Colors.BOLD + Colors.GREEN)}                   {colored("║", Colors.CYAN)}
{colored("║", Colors.CYAN)}    Type {colored("/help", Colors.YELLOW)} for commands            {colored("║", Colors.CYAN)}
{colored("╚════════════════════════════════════════╝", Colors.CYAN)}
"""
    print(banner)


def main():
    print_banner()

    while True:
        try:
            user_input = input(f"\n{colored('You:', Colors.BOLD + Colors.BLUE)} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{colored('Goodbye!', Colors.YELLOW)}")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.lower() == "exit":
            print(colored("Goodbye!", Colors.YELLOW))
            break

        if user_input.lower() == "/help":
            print(HELP_TEXT)
            continue

        if user_input.lower() == "/tools":
            print(TOOLS_TEXT)
            continue

        if user_input.lower() == "/clear":
            reset_conversation()
            print(colored("✓ Conversation cleared.", Colors.GREEN))
            continue

        # Run agent with spinner
        spinner = Spinner("Thinking")
        spinner.start()
        
        try:
            response = run_agent(user_input)
        except Exception as e:
            response = colored(f"Error: {str(e)}", Colors.RED)
        finally:
            spinner.stop()

        print(f"\n{colored('Agent:', Colors.BOLD + Colors.GREEN)} {response}")


if __name__ == "__main__":
    main()