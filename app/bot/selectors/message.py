import logging
from sqlmodel import select
from app.models import Message, User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.bot.exceptions import UserNotFoundException, MessageNotFoundException
from app.redis import AIORedis
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class MessageSelector:
    def __init__(
        self,
        session: AsyncSession,
        redis_service: Redis | None = None,
    ) -> None:
        self.session = session
        self.redis_service = redis_service if redis_service is not None else AIORedis
        self._user_key = "user_{user_id}"

    async def get_user(self, user_id: int) -> User:
        result = await self.session.exec(select(User).where(User.id == user_id))
        user = result.one_or_none()
        if user is None:
            raise UserNotFoundException(msg="Пользователь не найден")
        return user

    async def _get_message(self, user: User, message_id: int) -> Message:
        result = await self.session.exec(
            select(Message).where(
                Message.group_id == user.group_id,
                Message.id == message_id,
            )
        )
        message = result.one_or_none()
        if message is None:
            raise MessageNotFoundException(msg="Сообщение не найдено")
        return message

    async def _get_message_by_child_alias(
        self,
        user: User,
        last_message_id: int,
        child_alias: str,
    ) -> Message | None:
        """
        Получение сообщение по алиасу при переходе от одного сообщения к другому
        """
        result = await self.session.exec(
            select(Message).where(
                Message.group_id == user.group_id,
                Message.id == last_message_id,
            )
        )
        message = result.one_or_none()
        if message is None:
            return None

        new_message_id = message.childrens.get(child_alias)
        if new_message_id is None:
            return None

        return await self._get_message(user=user, message_id=new_message_id)

    async def _get_message_by_alias(
        self,
        user: User,
        tg_alias_name: str,
    ) -> Message | None:
        """
        Получение сообщения по алиасу
        """
        result = await self.session.exec(
            select(Message).where(
                Message.group_id == user.group_id,
                Message.tg_alias_name == tg_alias_name,
            )
        )
        return result.one_or_none()

    async def get_message(
        self,
        user: User,
        new_message_id: int | None,
        user_msg_text: str | None,
    ) -> tuple[Message, bool]:
        """
        Получение сообщение
        возращает два параметра: соответствующее сообщение и флаг что сообщения является предидущим
        """
        if new_message_id is not None:
            message = await self._get_message(user=user, message_id=new_message_id)
            return message, False

        if user_msg_text is not None:
            alias_message = await self._get_message_by_alias(
                user=user,
                tg_alias_name=user_msg_text,
            )
            if alias_message is not None:
                return alias_message, False

            last_message = await self._get_last_message(user_id=user.id)
            child_message = await self._get_message_by_child_alias(
                user=user,
                last_message_id=last_message.id,
                child_alias=user_msg_text,
            )
            return (
                (child_message, False)
                if child_message is not None
                else (last_message, True)
            )

        raise MessageNotFoundException(msg="Сообщение не найдено")

    async def get_message_by_id(self, message_id: int) -> Message:
        """
        Получение сообщения по найменованию
        """
        result = await self.session.exec(
            select(Message).where(Message.id == message_id)
        )
        message = result.one_or_none()
        if message is None:
            raise MessageNotFoundException(msg="Сообщение не найдено")

        return message

    async def save_last_message(self, user_id: int, message_id: int) -> None:
        await self.redis_service.set(self._user_key.format(user_id=user_id), message_id)

    async def _get_last_message(self, user_id: int) -> Message:
        message_id = await self.redis_service.get(
            name=self._user_key.format(user_id=user_id)
        )
        if message_id is None:
            raise MessageNotFoundException(msg="Сообщение не найдено")
        logger.error(f"user_id: {user_id}, message_id: {message_id}")
        return await self.get_message_by_id(message_id=int(message_id))
