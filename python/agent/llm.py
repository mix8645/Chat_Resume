import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from tasks.history_manage import rate_limiter

load_dotenv();

api_key = os.getenv("ANTHROPIC_API_KEY")

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    rate_limiter=rate_limiter,
)




