import json
from loader import redis


async def get_user_redis(telegram_id):
    key = f"user_data:{telegram_id}"
    user_data = await redis.get(key)
    if user_data:
        return json.loads(user_data)
    return None