import redis.asyncio as redis
from fastapi import Depends
from openai import OpenAI

from config import OPEN_AI_API_KEY
from repositories.redis_repository import RedisRepository
from repositories.github_repository import GitHubRepository
from repositories.open_ai_repository import OpenAIRepository
from services.review import ReviewService


async def get_redis_repository():
    """
   Dependency function to get an instance of RedisRepository.

   This function creates and returns a RedisRepository instance, which connects to
   the Redis server using the `redis.asyncio` library.

   Returns:
       RedisRepository: An instance of the RedisRepository.
   """
    return RedisRepository(await redis.Redis())

async def get_github_repository():
    """
    Dependency function to get an instance of GitHubRepository.

    This function creates and returns a GitHubRepository instance that will be used
    to fetch data from GitHub repositories.

    Returns:
        GitHubRepository: An instance of the GitHubRepository.
    """
    return GitHubRepository()

async def get_open_ai_repository():
    """
   Dependency function to get an instance of OpenAIRepository.

   This function creates and returns an OpenAIRepository instance, initializing it
   with the OpenAI API client using the configured API key.

   Returns:
       OpenAIRepository: An instance of the OpenAIRepository.
   """
    return OpenAIRepository(OpenAI(api_key=OPEN_AI_API_KEY))

async def get_review_service(
        redis_repository: RedisRepository = Depends(get_redis_repository),
        github_repository: GitHubRepository = Depends(get_github_repository),
        open_ai_repository: OpenAIRepository = Depends(get_open_ai_repository)
) -> ReviewService:
    """
    Dependency function to get an instance of ReviewService.

    This function creates and returns a ReviewService instance by injecting the necessary
    dependencies, including Redis, GitHub, and OpenAI repositories.

    Args:
        redis_repository (RedisRepository, optional): The RedisRepository instance.
        github_repository (GitHubRepository, optional): The GitHubRepository instance.
        open_ai_repository (OpenAIRepository, optional): The OpenAIRepository instance.

    Returns:
        ReviewService: An instance of the ReviewService.
    """
    return ReviewService(redis_repository, github_repository, open_ai_repository)
