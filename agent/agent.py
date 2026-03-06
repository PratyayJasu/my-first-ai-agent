import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .tools import TOOLS
from .prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_agent(user_input):

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    message = response.choices[0].message.content

    try:
        action = json.loads(message)

        tool_name = action["tool"]
        args = action["args"]

        tool = TOOLS[tool_name]

        result = tool(**args)

        return f"{result}"

    except Exception as e:
        return message