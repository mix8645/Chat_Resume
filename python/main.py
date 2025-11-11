import os
from dotenv import load_dotenv
from agent.prompt import SYSTEM_PROMPT
from langchain import ChatAnthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")


