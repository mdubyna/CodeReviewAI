from openai import OpenAI

from tenacity import (
  retry,
  stop_after_attempt,
  wait_random_exponential,
)


class OpenAIRepository:
    def __init__(self, open_ai_client: OpenAI):
        self.open_ai_client = open_ai_client

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    async def completion_with_backoff(self, **kwargs):
        return await self.open_ai_client.chat.completions.create(**kwargs)
