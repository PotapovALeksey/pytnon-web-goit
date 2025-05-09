import redis.asyncio as redis

from src.config.config import config


def get_cache():
    return redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PASSWORD)
