import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv();

api_key = os.getenv("ANTHROPIC_API_KEY")

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2
)


