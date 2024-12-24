from logging import getLogger

import redis.asyncio


logger = getLogger(__name__)

class RedisRepository:
    """
    A repository for interacting with a Redis cache.

    Provides methods for setting and retrieving values from a Redis instance.
    """
    def __init__(self, redis_client: redis.asyncio.Redis):
        """
        Initialize the RedisRepository with a Redis client.

        Args:
            redis_client (redis.asyncio.Redis): An asynchronous Redis client instance.
        """
        self.redis_client = redis_client

    async def get(self, key: str) -> str | None:
        """
        Retrieve a value from Redis by its key.

        Logs the operation and returns the value if it exists, or `None` otherwise.

        Args:
            key (str): The key to fetch the value for.

        Returns:
            str | None: The value associated with the key, or `None` if the key does not exist.
        """
        value = await self.redis_client.get(key)
        logger.info("Get value from Redis cache by key: %s. Value: %s", key, value)
        return value if value else None

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        """
        Store a key-value pair in Redis with an optional time-to-live (TTL).

        Logs the operation and sets the value with the specified TTL.

        Args:
            key (str): The key to set in the cache.
            value (str): The value to associate with the key.
            ttl (int, optional): Time-to-live for the key in seconds. Defaults to 3600 seconds (1 hour).
        """
        logger.info("Set key: %s, value: %s to Redis cache.", key, value)
        await self.redis_client.set(key, value, ex=ttl)
