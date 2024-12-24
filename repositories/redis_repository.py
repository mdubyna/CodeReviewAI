from logging import getLogger

import redis.asyncio


logger = getLogger(__name__)

class RedisRepository:
    def __init__(self, redis_client: redis.asyncio.Redis):
        self.redis_client = redis_client

    async def get(self, key: str) -> str | None:
        value = await self.redis_client.get(key)
        logger.info("Get value from Redis cache by key: %s. Value: %s", key, value)
        return value if value else None

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        logger.info("Set key: %s, value: %s to Redis cache.", key, value)
        await self.redis_client.set(key, value, ex=ttl)
