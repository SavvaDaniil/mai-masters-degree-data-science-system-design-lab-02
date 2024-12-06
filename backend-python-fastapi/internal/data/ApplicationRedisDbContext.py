
import os
import redis

DATABASE_REDIS_URL = os.getenv("DATABASE_REDIS_URL", "redis://cache:6379/0")

class ApplicationRedisDbContext():

    def get_client(self):
        return redis.from_url(DATABASE_REDIS_URL, decode_responses=True)