import redis
from redis_lru import RedisLRU

client = redis.Redis(host="0.0.0.0", port=6379)

cache = RedisLRU(client)
