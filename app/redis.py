"""Reids configuration"""
from redis.asyncio import Redis

from config.settings import settings

AIORedis = Redis.from_url(url=str(settings.REDIS_URL), decode_responses=True)
