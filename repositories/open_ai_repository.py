from openai import OpenAI

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


class OpenAIRepository:
    """
    A repository for interacting with OpenAI's API.

    Provides methods to handle OpenAI API requests with built-in retry
    logic for handling transient errors.
    """

    def __init__(self, open_ai_client: OpenAI):
        """
        Initialize the OpenAIRepository with an OpenAI client.

        Args:
            open_ai_client (OpenAI): An instance of the OpenAI client.
        """
        self.open_ai_client = open_ai_client

    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
        reraise=True,
    )
    async def completion_with_backoff(self, **kwargs):
        """
        Make a chat completion request to the OpenAI API with retry logic.

        Retries the request with exponential backoff in case of transient
        errors (e.g., network issues or rate limits).

        Args:
            **kwargs: Arbitrary keyword arguments to be passed to the
                      `chat.completions.create` method.

        Returns:
            dict: The response from the OpenAI API.

        Raises:
            Exception: If all retry attempts fail, the exception will be propagated.
        """
        return await self.open_ai_client.chat.completions.create(**kwargs)
