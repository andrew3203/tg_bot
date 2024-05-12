from sqlmodel import select
from app.models import Message, User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.bot.exceptions import UserNotFoundException, MessageNotFoundException


class MessageSelector:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(self, user_id: int) -> User:
        result = await self.session.exec(select(User).where(User.id == user_id))
        user = result.one_or_none()
        if user is None:
            raise UserNotFoundException(msg="Пользователь не найден")
        return user

    async def get_message(self, user: User, message_id: int):
        """
        Получение сообщение
        """
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

    async def get_message_by_child_alias(
        self, user: User, prev_message_id: int, child_alias: str
    ):
        """
        Получение сообщение по алиасу при переходе от одного сообщения к другому
        """
        result = await self.session.exec(
            select(Message).where(
                Message.group_id == user.group_id,
                Message.id == prev_message_id,
            )
        )
        message = result.one_or_none()
        if message is None:
            raise MessageNotFoundException(msg="Сообщение не найдено")

        new_message_id = message.childrens.get(child_alias)
        if new_message_id is None:
            raise MessageNotFoundException(msg="Сообщение не найдено")

        return await self.get_message(user=user, message_id=new_message_id)

    async def get_message_by_alias(self, user: User, tg_alias_name: str):
        """
        Получение сообщения по алиасу
        """
        result = await self.session.exec(
            select(Message).where(
                Message.group_id == user.group_id,
                Message.tg_alias_name == tg_alias_name,
            )
        )
        message = result.one_or_none()
        if message is None:
            raise MessageNotFoundException(msg="Сообщение не найдено")

        return message

    async def get_message_by_id(self, message_id: int):
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
