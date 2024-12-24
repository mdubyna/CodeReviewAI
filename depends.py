import redis.asyncio as redis
from fastapi import Depends
from openai import OpenAI

from config import OPEN_AI_API_KEY
from repositories.redis_repository import RedisRepository
from repositories.github_repository import GitHubRepository
from repositories.open_ai_repository import OpenAIRepository
from services.review import ReviewService


async def get_redis_repository():
    return RedisRepository(await redis.Redis())

async def get_github_repository():
    return GitHubRepository()

async def get_open_ai_repository():
    return OpenAIRepository(OpenAI(api_key=OPEN_AI_API_KEY))

async def get_review_service(
        redis_repository: RedisRepository = Depends(get_redis_repository),
        github_repository: GitHubRepository = Depends(get_github_repository),
        open_ai_repository: OpenAIRepository = Depends(get_open_ai_repository)
) -> ReviewService:
    return ReviewService(redis_repository, github_repository, open_ai_repository)
