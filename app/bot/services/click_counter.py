from app.models import Message, User
from app.redis import AIORedis
from redis.asyncio import Redis
from app.json import json


class ClickCounterService:
    def __init__(self, redis_service: Redis | None = None) -> None:
        self.redis_service = redis_service if redis_service is not None else AIORedis
        self._message_uclick_key = "message_user_uclick_list_{message_id}"
        self._action_uclick_key = "action_user_uclick_list_{action_id}"

    async def _count_unclick(self, uclick_amount: int, user_id: int, key: str) -> int:
        result = await self.redis_service.get(name=key)
        user_id_list = set() if result is None else set(json.loads(result))
        if user_id not in user_id_list:
            uclick_amount += 1
            user_id_list.add(user_id)
        await self.redis_service.set(name=key, value=json.dumps(user_id_list))
        return uclick_amount

    async def count_message_unclick(self, message: Message, user: User) -> Message:
        key = self._message_uclick_key.format(message_id=message.id)
        uclick_amount = await self._count_unclick(
            uclick_amount=message.uclick_amount,
            user_id=user.id,
            key=key,
        )
        message.uclick_amount = uclick_amount
        return message
